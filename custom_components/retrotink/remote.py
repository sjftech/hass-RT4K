"""RetroTINK-4K remote entity (USB serial or DonutShop Wi-Fi)."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any, Iterable

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    COMMAND_MAP,
    CONF_CONNECTION_TYPE,
    CONF_DEVICE_MODEL,
    CONF_HOST,
    CONF_SERIAL_PORT,
    CONNECTION_DONUTSHOP,
    CONNECTION_SERIAL,
    DOMAIN,
    POWER_OFF_CMD,
    POWER_ON_CMD,
)
from .transport import (
    DonutShopTransport,
    SerialTransport,
    TransportError,
    power_state_to_bool,
)

_LOGGER = logging.getLogger(__name__)

# Only used by the DonutShop connection; USB serial has nothing to poll.
SCAN_INTERVAL = timedelta(seconds=15)

# After a power command, ignore polled power state for this long so the
# entity doesn't flip back while the RetroTINK is still booting / going to sleep.
POWER_GRACE_SECONDS = 20


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the RetroTINK remote from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    connection = config.get(CONF_CONNECTION_TYPE, CONNECTION_SERIAL)

    if connection == CONNECTION_DONUTSHOP:
        transport = DonutShopTransport(async_get_clientsession(hass), config[CONF_HOST])
        name = config_entry.title
    else:
        transport = SerialTransport(config[CONF_SERIAL_PORT])
        name = config[CONF_DEVICE_MODEL]

    async_add_entities(
        [RetroTINKRemote(name, config[CONF_DEVICE_MODEL], transport, config_entry.entry_id)],
        True,
    )


class RetroTINKRemote(RemoteEntity):
    """A RetroTINK-4K exposed as a Home Assistant remote."""

    def __init__(
        self,
        name: str,
        device_model: str,
        transport: SerialTransport | DonutShopTransport,
        entry_id: str,
    ) -> None:
        self._attr_name = name
        self._device_model = device_model
        self._transport = transport
        self._is_donutshop = isinstance(transport, DonutShopTransport)
        self._attr_unique_id = f"{entry_id}_remote"
        self._attr_is_on = False
        self._attr_should_poll = self._is_donutshop
        self._attr_extra_state_attributes: dict[str, Any] = {}
        self._last_power_cmd: float = 0.0

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if isinstance(self._transport, SerialTransport):
            await self.hass.async_add_executor_job(self._transport.configure)

    @property
    def device_info(self):
        info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._attr_name,
            "manufacturer": "RetroTINK",
            "model": self._device_model,
        }
        if self._is_donutshop:
            info["configuration_url"] = self._transport.base_url
        return info

    # ------------------------------------------------------------------ state

    async def async_update(self) -> None:
        """Poll the DonutShop for the RetroTINK's real state."""
        if not self._is_donutshop:
            return
        try:
            data = await self._transport.status()
        except TransportError as err:
            if self._attr_available:
                _LOGGER.warning("DonutShop unreachable: %s", err)
            self._attr_available = False
            return

        self._attr_available = True
        if data is None:
            # Busy (e.g. WebCtl page open in a browser) or firmware < 0.7.25:
            # keep the last known / assumed state.
            return

        rt = data.get("retrotink", {}) or {}
        ds = data.get("donutshop", {}) or {}

        power = power_state_to_bool(rt.get("power_state"))
        in_grace = (
            asyncio.get_running_loop().time() - self._last_power_cmd
            < POWER_GRACE_SECONDS
        )
        if power is not None and not in_grace:
            self._attr_is_on = power

        self._attr_extra_state_attributes = {
            "power_state": rt.get("power_state"),
            "profile": rt.get("profile"),
            "input": rt.get("active_video_input"),
            "output": rt.get("active_video_output"),
            "retrotink_connected": ds.get("retrotink_connected"),
            "donutshop_ip": ds.get("ip"),
            "donutshop_rssi": ds.get("rssi"),
        }

    # --------------------------------------------------------------- commands

    async def _send(self, command: str) -> None:
        _LOGGER.debug("Sending to %s: %s", self._attr_name, command)
        try:
            if isinstance(self._transport, SerialTransport):
                await self.hass.async_add_executor_job(self._transport.send, command)
            else:
                await self._transport.send(command)
        except TransportError as err:
            _LOGGER.error("Error sending %r to %s: %s", command, self._attr_name, err)
            raise

    async def _set_power(self, on: bool) -> None:
        await self._send(POWER_ON_CMD if on else f"remote {POWER_OFF_CMD}")
        self._last_power_cmd = asyncio.get_running_loop().time()
        self._attr_is_on = on
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._set_power(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._set_power(False)

    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send one or more commands.

        - Known button names (menu, up, prof3, 4k, ...) are sent as "remote <cmd>".
        - power_on / power_off / power are the power commands.
        - Anything containing a space is sent exactly as written, e.g.
          "SVS NEW INPUT=1" or "remote prof12".
        """
        num_repeats = kwargs.get("num_repeats", 1)
        delay_secs = kwargs.get("delay_secs", 0.4)
        commands = list(command)

        for repeat in range(num_repeats):
            for index, cmd in enumerate(commands):
                key = cmd.strip().lower()
                if key in ("power_on", "pwr_on"):
                    await self._set_power(True)
                elif key in ("power_off", "power", "pwr"):
                    await self._set_power(False)
                elif " " in cmd.strip():
                    await self._send(cmd.strip())
                else:
                    await self._send(f"remote {COMMAND_MAP.get(key, key)}")

                last = repeat == num_repeats - 1 and index == len(commands) - 1
                if delay_secs > 0 and not last:
                    await asyncio.sleep(delay_secs)
