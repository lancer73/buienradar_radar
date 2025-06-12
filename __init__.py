"""Buienradar Regenradar integration."""
from **future** import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant

from .const import (
DOMAIN,
DEFAULT_NAME,
CONF_IMAGE_REFRESH_SECONDS,
RADAR_URL,
)

_LOGGER = logging.getLogger(**name**)

# List of platforms to set up

PLATFORMS = [Platform.CAMERA]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Buienradar Regenradar from a config entry."""
    _LOGGER.debug("Setting up Buienradar Regenradar integration")

    # Store the config entry data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to camera platform using the new API
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """"Unload a config entry.""""
    _LOGGER.debug("Unloading Buienradar Regenradar integration")

    # Unload the camera platform
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)