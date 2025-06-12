"""Camera platform for Buienradar Regenradar integration."""
from **future** import annotations

import logging
import asyncio
from datetime import timedelta
from typing import Optional

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util

from .const import DOMAIN, DEFAULT_NAME, CONF_IMAGE_REFRESH_SECONDS, RADAR_URL

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the Buienradar camera from a config entry."""
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    refresh_seconds = entry.data.get(CONF_IMAGE_REFRESH_SECONDS, 300)

    # Get refresh from options if available
    if entry.options:
        refresh_seconds = entry.options.get(CONF_IMAGE_REFRESH_SECONDS, refresh_seconds)

    session = async_get_clientsession(hass)

    async_add_entities([BuienradarCamera(hass, name, refresh_seconds, session, entry.entry_id)])

class BuienradarCamera(Camera):
    """Representation of the Buienradar rain radar camera."""

    def __init__(self, hass, name, refresh_seconds, session, entry_id=None):
        """Initialize Buienradar camera component."""
        super().__init__()
        self._hass = hass
        self._name = name
        self._image = None
        self._refresh_seconds = refresh_seconds
        self._session = session
        self._attr_content_type = 'image/png'
        self._entry_id = entry_id
    
        # Fix for unique_id - ensure it always has a value
        if entry_id:
            self._attr_unique_id = f"buienradar_radar_{entry_id}"
        else:
            self._attr_unique_id = "buienradar_regenradar"
        
        # Set up a scheduled task to refresh the image periodically
        self._remove_listener = None

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return {
            "refresh_seconds": self._refresh_seconds,
        }

    @property
    def frame_interval(self):
        """Return the interval between frames."""
        return timedelta(seconds=self._refresh_seconds)

    async def async_added_to_hass(self):
        """Set up a timer when added to hass."""
        await super().async_added_to_hass()
    
        # Schedule regular updates based on refresh_seconds
        async def _scheduled_refresh(*_):
            """Refresh camera image on schedule determined by refresh_seconds."""
            await self.async_update_ha_state(True)

    # Fixed: Use the imported async_track_time_interval instead of accessing via hass.helpers
    self._remove_listener = async_track_time_interval(
        self.hass, _scheduled_refresh, timedelta(seconds=self._refresh_seconds)
    )

    async def async_will_remove_from_hass(self):
        """Clean up after entity is removed."""
        await super().async_will_remove_from_hass()
        if self._remove_listener is not None:
            self._remove_listener()

    async def async_camera_image(self, width: Optional[int] = None, height: Optional[int] = None) -> Optional[bytes]:
        """Return a still image from the camera."""
        try:
            _LOGGER.debug("Fetching new radar image from Buienradar")
        
            # Add timestamp to URL to prevent caching issues
            timestamp = dt_util.now().strftime('%Y%m%d%H%M%S')
            url = f"{RADAR_URL}?time={timestamp}"
        
            async with async_timeout.timeout(10):
                response = await self._session.get(url)
                if response.status == 200:
                    self._image = await response.read()
                    return self._image
                else:
                    _LOGGER.error("Error fetching Buienradar image: %s", response.status)
                    return self._image
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("Error retrieving Buienradar image: %s", error)
            return self._image

    async def async_update(self):
        """Refresh the image."""
        # This explicitly refreshes the image when Home Assistant calls for an update
        await self.async_camera_image()