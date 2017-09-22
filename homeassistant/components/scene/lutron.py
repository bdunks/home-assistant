"""
Support for Lutron scenes.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/scene.lutron/
"""
import asyncio
import logging

from homeassistant.components.scene import Scene
from homeassistant.components.lutron import (
    LutronDevice, LUTRON_DEVICES, LUTRON_CONTROLLER)
from homeassistant.const import (
    STATE_OFF, STATE_ON
)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['lutron']


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Lutron Scene."""
    devs = []
    for (keypad, button) in hass.data[LUTRON_DEVICES]['scene']:
        dev = LutronScene(keypad, button, hass.data[LUTRON_CONTROLLER])
        devs.append(dev)

    add_devices(devs, True)
    return True


class LutronScene(LutronDevice, Scene):
    """Representation of a Lutron scene."""

    def __init__(self, keypad, button, controller):
        """Initialize the Lutron scene."""
        self._button = button
        self._keypad = keypad
        LutronDevice.__init__(self, "", button, controller)

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
        state = STATE_OFF
        if self._button.led.state:
            state = STATE_ON
        return state

    def activate(self, **kwargs):
        """Activate the scene."""
        self._keypad.press(self._button)
