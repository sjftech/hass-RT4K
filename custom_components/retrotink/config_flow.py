"""Config flow for RetroTINK-4K (USB serial or DonutShop Wi-Fi)."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_CONNECTION_TYPE,
    CONF_DEVICE_MODEL,
    CONF_HOST,
    CONF_SERIAL_PORT,
    CONNECTION_DONUTSHOP,
    CONNECTION_SERIAL,
    DEFAULT_DONUTSHOP_HOST,
    DEVICE_MODELS,
    DOMAIN,
)
from .transport import DonutShopTransport, SerialTransport

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RetroTINK-4K."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Ask how the RetroTINK is connected."""
        return self.async_show_menu(
            step_id="user",
            menu_options=[CONNECTION_DONUTSHOP, CONNECTION_SERIAL],
        )

    async def async_step_donutshop(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure a RetroTINK reached through a DonutShop dongle."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            transport = DonutShopTransport(async_get_clientsession(self.hass), host)
            info = None
            try:
                if not await transport.test():
                    errors["base"] = "cannot_connect_donutshop"
                else:
                    info = await transport.info()
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if not errors:
                hostname = (info or {}).get("donutshop", {}).get("hostname") or host
                await self.async_set_unique_id(f"donutshop_{hostname.lower()}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"{user_input[CONF_DEVICE_MODEL]} ({hostname})",
                    data={
                        CONF_CONNECTION_TYPE: CONNECTION_DONUTSHOP,
                        CONF_HOST: host,
                        CONF_DEVICE_MODEL: user_input[CONF_DEVICE_MODEL],
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_MODEL): vol.In(DEVICE_MODELS),
                vol.Required(CONF_HOST, default=DEFAULT_DONUTSHOP_HOST): str,
            }
        )
        return self.async_show_form(
            step_id="donutshop", data_schema=schema, errors=errors
        )

    async def async_step_serial(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure a RetroTINK plugged into this machine by USB."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_SERIAL_PORT])
            self._abort_if_unique_id_configured()

            transport = SerialTransport(user_input[CONF_SERIAL_PORT])
            try:
                ok = await self.hass.async_add_executor_job(transport.test)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                if not ok:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=user_input[CONF_DEVICE_MODEL],
                        data={CONF_CONNECTION_TYPE: CONNECTION_SERIAL, **user_input},
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_MODEL): vol.In(DEVICE_MODELS),
                vol.Required(CONF_SERIAL_PORT): str,
            }
        )
        return self.async_show_form(step_id="serial", data_schema=schema, errors=errors)
