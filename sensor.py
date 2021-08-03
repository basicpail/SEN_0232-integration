import logging
from datetime import timedelta
from ast import literal_eval


from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import ATTR_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICES

from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS
)

from .const import DOMAIN,CONF_DEVICEID,NOISE_SENSOR

ATTRIBUTION = ("NOISE_SENSOR_SEN0232")

DEFAULT_NAME = "SEN0232"

_LOGGER = logging.getLogger(__name__)

#SCAN_INTERVAL = timedelta(seconds=30)

STATUS_CATEGORY = [
    "decibel"
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    
    coordinator = hass.data[DOMAIN][NOISE_SENSOR]
    #_LOGGER.info(f"navien coordinator : {coordinator}")

    entities = []
    for i,status_category in enumerate(STATUS_CATEGORY):
        entities.append(LuxBaseSensor(coordinator, config_entry.data, status_category))

    async_add_entities(entities)
    
    #entities.append(NavienBaseSensor(coordinator,config_entry.data))

class LuxBaseSensor(CoordinatorEntity,Entity):

    def __init__(self, coordinator, config, STATUS_CATEGORY):
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._config = config
        self._data_type = STATUS_CATEGORY
        #self._current_operationmode = NavienAirone(deviceid=self._config.get(CONF_DEVICEID))

    @property
    def unique_id(self):
        """Return unique ID."""
        _LOGGER.info(f"navien def unique_id {self._config[CONF_DEVICEID]}{self._data_type}")
        return f"{self._config[CONF_DEVICEID]}_{self._data_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self._config.get(CONF_DEVICEID)
        _LOGGER.info(f"navien def name {DEFAULT_NAME} {self._data_type}")
        return f"{DEFAULT_NAME}_{self._data_type}"

    @property
    def state(self):
        # if self._hass_states == None:
        #     pass
        # else:
            # _LOGGER.info(f"debugmsg1 {self._hass_states.get('switch.42f52007eefa')}")
            # _LOGGER.info(f"debugmsg2 {self._hass_states.get('switch.42f52007eefa').state}")
            # _LOGGER.info(f"debugmsg3 {self._hass_states.get('switch.42f52007eefa').attributes}")
            # _LOGGER.info(f"debugmsg3 {self._hass_states.get('switch.42f52007eefa').attributes['current_power_w']}")
            # _LOGGER.info(f"debugmsg3 {self._hass_states.get('switch.42f52007eefa').attributes['today_energy_kwh']}")

        if self.coordinator.data.current_status_data == None:
            return "uploading.."


        if self._data_type == "decibel":
            # self._hass_states.set(
            #         entity_id = 'sensor.sen0232_smartplug_powermeter',
            #         new_state = self._hass_states.get('switch.42f52007eefa').attributes['current_power_w']
            #     )

            _LOGGER.info(f"noisesensordebug self.coordinator.data.current_status_data.decode() : {self.coordinator.data.current_status_data.decode()}")
            return self.coordinator.data.current_status_data.decode()

            
    @property
    def unit_of_measurement(self):
        #if self.coordinator.data.current_status_data == None:
        #    return 
        #if self._data_type == "decibel":
        #    return SIGNAL_STRENGTH_DECIBELS
        return SIGNAL_STRENGTH_DECIBELS

    @property
    def attribution(sefl):
        return ATTRIBUTION

    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN,)},
            "manufacturer": "DFROBOT",
            "model": "SEN0232",
            "default_name": "SEN0232",
            "entry_type": "device", ##
        }
