"""
Support for Lutron scenes.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/scene.lutron/
"""
import logging

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.components.scene import Scene
from homeassistant.components.lutron import (
    LutronDevice, LUTRON_DEVICES, LUTRON_CONTROLLER, DOMAIN)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['lutron']

ATTR_BUTTON_NAME = 'button_name'
ATTR_KEYPAD_NAME = 'keypad_name'

EVENT_SCENE_ACTIVATED = 'lutron.scene_activated'

STATE_ACTIVE = 'active'
STATE_INACTIVE = 'inactive'


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Lutron Scene."""
    devs = []
    for button in hass.data[LUTRON_DEVICES]['scene']:
        dev = LutronScene(button, hass)
        devs.append(dev)

    add_devices(devs, True)
    return True


class LutronScene(LutronDevice, Scene):
    """Representation of a Lutron scene."""

    def __init__(self, button, hass):
        """Initialize the Lutron scene."""
        LutronDevice.__init__(self, None, button, hass.data[LUTRON_CONTROLLER])
        hass.data[DOMAIN]['entities']['scene'].append(self)

    @property
    def name(self):
        """Return the name of the scene."""
        return self._lutron_device.name

    @property
    def should_poll(self):
        """Return that polling is not necessary."""
        return False

    @property
    def state(self):
        """Return the state of the scene."""
        state = STATE_INACTIVE
        if self._lutron_device.led.state:
            state = STATE_ACTIVE
        return state

    def _update_callback(self, _device):
        self.hass.bus.fire(EVENT_SCENE_ACTIVATED, {
            ATTR_ENTITY_ID: self.entity_id,
            ATTR_BUTTON_NAME: self._lutron_device.name,
        })
        return LutronDevice._update_callback(self, _device)

    def activate(self, **kwargs):
        """Activate the scene."""
        self._lutron_device.press()
