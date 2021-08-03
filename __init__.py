from datetime import timedelta
import logging
from random import randrange

from noisesensor.noisesensor import NoiseSensor

from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.restore_state import RestoreEntity



from .const import DOMAIN,CONF_DEVICEID,SUPPORT_TYPE,NOISE_SENSOR
_LOGGER = logging.getLogger(__name__)



async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass, config_entry):
    coordinator = NoiseSensorDataUpdateCoordinator(hass, config_entry)
    custom_config = []
    custom_config.append(coordinator)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady
    #hass.data[DOMAIN][config_entry.entry_id].add(custom_config)
    #hass.data[DOMAIN][config_entry.entry_id] = coordinator
    hass.data[DOMAIN][NOISE_SENSOR] = coordinator
   

    for domain in SUPPORT_TYPE:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, domain) #whats config_entry exactly
        )

    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    for domain in SUPPORT_TYPE:
        await hass.config_entries.async_forward_entry_unload(config_entry, domain)
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return True


class NoiseSensorDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, config_entry):
        self._unsub_track_home = None
        self.statusvalue = NoiseStatusData(hass, config_entry.data)
        self.statusvalue.init_data()

        update_interval = timedelta(seconds=60)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self):
        _LOGGER.info("function _async_update_data was called")
        print("_async_update_data was called")
        try:
            return await self.statusvalue.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err


class NoiseStatusData:
    def __init__(self, hass, config):
        self.hass = hass
        self._config = config
        self.current_status_data = {}

    def init_data(self):
        """get the coordinates."""
        _LOGGER.info(f"navien self._config.get(CONF_DEVICEID): {self._config.get(CONF_DEVICEID)}") #CONF_DEVICE : userinput
        self._data_sub = NoiseSensor(
                hass = self.hass,
                brokeraddr = '192.168.97.118',
                port = 1883,
                topic = "IOT/data/noise",
                deviceid=self._config.get(CONF_DEVICEID),
                username = "kict",
                password = "kict",
                )
        self._data_sub.sub_threading()
            
        self.current_status_data = self._data_sub._payload

    async def fetch_data(self):
        """Fetch data from API"""
        #await self._navien_data.fetching_data()        
        self.current_status_data = self._data_sub._payload
        return self
