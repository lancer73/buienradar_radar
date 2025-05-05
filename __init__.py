"""
Buienradar Rain Radar Integration for Home Assistant
Author: Claude
Date: 2025-05-05
"""
import logging
import voluptuous as vol
from datetime import timedelta
import asyncio
import aiohttp
import async_timeout
import homeassistant.helpers.config_validation as cv
from homeassistant.components.camera import Camera, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "buienradar_radar"
DEFAULT_NAME = 'Buienradar Regenradar'
CONF_IMAGE_REFRESH_SECONDS = 'image_refresh_seconds'

# URL voor de Buienradar regenradar afbeelding
RADAR_URL = 'https://api.buienradar.nl/image/1.0/radarmapnl'

# Platform schema configuratie (voor oude configuration.yaml methode)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_IMAGE_REFRESH_SECONDS, default=300): cv.positive_int,
})

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Buienradar Rain Radar component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Buienradar from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    await hass.config_entries.async_forward_entry_setup(entry, "camera")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["camera"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Buienradar camera platform via configuration.yaml."""
    name = config.get(CONF_NAME)
    refresh_seconds = config.get(CONF_IMAGE_REFRESH_SECONDS)
    
    session = async_get_clientsession(hass)
    
    async_add_entities([BuienradarCamera(hass, name, refresh_seconds, session)])

class BuienradarCamera(Camera):
    """Representation of the Buienradar rain radar camera."""

    def __init__(self, hass, name, refresh_seconds, session):
        """Initialize Buienradar camera component."""
        super().__init__()
        self._hass = hass
        self._name = name
        self._image = None
        self._refresh_seconds = refresh_seconds
        self._session = session
        self._attr_content_type = 'image/png'
        self._remove_listener = None

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of this camera."""
        return f"buienradar_rain_radar"

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

        # Schedule the first update in 1 second
        self._remove_listener = async_track_time_interval(
            self.hass, _scheduled_refresh, timedelta(seconds=self._refresh_seconds)
        )

    async def async_will_remove_from_hass(self):
        """Clean up after entity is removed."""
        await super().async_will_remove_from_hass()
        if self._remove_listener is not None:
            self._remove_listener()

    async def async_camera_image(self, width=None, height=None):
        """Return a still image from the camera."""
        try:
            _LOGGER.debug("Fetching new radar image from Buienradar")
            async with async_timeout.timeout(10):
                response = await self._session.get(RADAR_URL)
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
        await self.async_camera_image()