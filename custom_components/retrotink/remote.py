"""Support for RetroTINK serial remote control."""
from __future__ import annotations

import logging
from typing import Any, Iterable
import subprocess

import serial

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_SERIAL_PORT, CONF_DEVICE_MODEL, COMMAND_MAP, POWER_ON_CMD, POWER_OFF_CMD

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the RetroTINK remote from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities(
        [RetroTINKRemote(
            config[CONF_DEVICE_MODEL],  # Use device model as name
            config[CONF_DEVICE_MODEL],
            config[CONF_SERIAL_PORT],
            config_entry.entry_id
        )],
        True,
    )


class RetroTINKRemote(RemoteEntity):
    """Representation of a RetroTINK remote control."""

    def __init__(
        self,
        name: str,
        device_model: str,
        serial_port: str,
        entry_id: str,
    ) -> None:
        """Initialize the RetroTINK remote."""
        self._attr_name = name
        self._device_model = device_model
        self._serial_port = serial_port
        self._attr_unique_id = f"{entry_id}_remote"
        self._attr_is_on = False  # Track power state based on commands sent
        self._serial = None
        
    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass - configure serial port."""
        await super().async_added_to_hass()
        # Configure the serial port with proper settings
        await self.hass.async_add_executor_job(self._configure_serial_port)

    def _configure_serial_port(self) -> None:
        """Configure serial port using stty."""
        try:
            cmd = f"stty -F {self._serial_port} 115200 cs8 -cstopb -parenb"
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            _LOGGER.debug(f"Configured serial port {self._serial_port}")
        except subprocess.CalledProcessError as err:
            _LOGGER.warning(f"Could not configure serial port {self._serial_port}: {err}")

    @property
    def device_info(self):
        """Return device information about this RetroTINK."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._attr_name,
            "manufacturer": "RetroTINK",
            "model": self._device_model,
        }

    def _send_command(self, command: str, is_power_on: bool = False) -> bool:
        """Send a command to the RetroTINK via serial.
        
        Args:
            command: The command to send (will be prefixed with 'remote ' unless it's power on)
            is_power_on: If True, command is 'pwr on' and sent without 'remote ' prefix
        """
        try:
            # Open serial connection with proper settings
            ser = serial.Serial(
                self._serial_port,
                115200,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=1
            )
            
            # Format command - only 'pwr on' doesn't get 'remote' prefix
            if is_power_on:
                cmd = f"{command}\n"
            else:
                cmd = f"remote {command}\n"
                
            _LOGGER.debug(f"Sending command to {self._attr_name}: {cmd.strip()}")
            ser.write(cmd.encode('ascii'))
            
            # Close connection
            ser.close()
            return True
            
        except serial.SerialException as err:
            _LOGGER.error(f"Error sending command to {self._attr_name}: {err}")
            return False
        except Exception as err:
            _LOGGER.error(f"Unexpected error sending command to {self._attr_name}: {err}")
            return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the remote on (power on the device)."""
        result = await self.hass.async_add_executor_job(
            self._send_command, POWER_ON_CMD, True
        )
        if result:
            self._attr_is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the remote off (power off the device)."""
        result = await self.hass.async_add_executor_job(
            self._send_command, POWER_OFF_CMD, False
        )
        if result:
            self._attr_is_on = False
            self.async_write_ha_state()

    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send a command to the device.
        
        Args:
            command: A list of commands to send.
            **kwargs: Additional arguments (num_repeats, delay_secs, etc.)
        """
        num_repeats = kwargs.get("num_repeats", 1)
        delay_secs = kwargs.get("delay_secs", 0.4)
        
        for _ in range(num_repeats):
            for cmd in command:
                # Check if this is a power command
                is_power_on = False
                actual_cmd = cmd.lower()
                
                if actual_cmd in ["power_on", "pwr_on"]:
                    actual_cmd = POWER_ON_CMD
                    is_power_on = True
                    self._attr_is_on = True
                elif actual_cmd in ["power_off", "power", "pwr"]:
                    actual_cmd = POWER_OFF_CMD
                    is_power_on = False  # This will get 'remote' prefix
                    self._attr_is_on = False
                else:
                    # Map standard remote commands to RetroTINK commands
                    actual_cmd = COMMAND_MAP.get(actual_cmd, actual_cmd)
                
                # Send the command
                await self.hass.async_add_executor_job(
                    self._send_command, actual_cmd, is_power_on
                )
                
                # Update state if power changed
                if actual_cmd in [POWER_ON_CMD, POWER_OFF_CMD]:
                    self.async_write_ha_state()
                
                # Add delay between commands if there are more to send
                if delay_secs > 0 and (len(command) > 1 or num_repeats > 1):
                    await self.hass.async_add_executor_job(
                        lambda: __import__('time').sleep(delay_secs)
                    )
