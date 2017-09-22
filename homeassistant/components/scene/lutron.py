"""
Support for Lutron scenes.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/scene.lutron/
"""
import asyncio
import logging

from homeassistant.components.scene import Scene
from homeassistant.components.lutron import (
    LutronDevice, LUTRON_DEVICES, LUTRON_CONTROLLER, DOMAIN)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['lutron']

STATE_ACTIVE = 'active'
STATE_INACTIVE = 'inactive'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Lutron Scene."""
    devs = []
    for (keypad, button) in hass.data[LUTRON_DEVICES]['scene']:
        dev = LutronScene(keypad, button, hass)
        devs.append(dev)

    add_devices(devs, True)
    return True


class LutronScene(LutronDevice, Scene):
    """Representation of a Lutron scene."""

    def __init__(self, keypad, button, hass):
        """Initialize the Lutron scene."""
        self._button = button
        self._keypad = keypad
        LutronDevice.__init__(self, "", keypad, hass.data[LUTRON_CONTROLLER])
        hass.data[DOMAIN]['entities']['scene'].append(self)

    @property
    def name(self):
        """Return the name of the scene."""
        return self._button.name

    @property
    def should_poll(self):
        """Return that polling is not necessary."""
        return False

    @property
    def state(self):
        """Return the state of the scene."""
        state = STATE_INACTIVE
        if self._button.led.state:
            state = STATE_ACTIVE
        return state

    def raise_activate_event(self):
        _LOGGER.debug("Raising activate for {}".format(self.name))

    def activate(self, **kwargs):
        """Activate the scene."""
        self._keypad.press(self._button)
