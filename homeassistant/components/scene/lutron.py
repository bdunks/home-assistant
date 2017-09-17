"""
Support for Lutron scenes.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/scene.lutron/
"""
import logging

from homeassistant.components.scene import Scene
from homeassistant.components.lutron import LUTRON_DEVICES

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['lutron']


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Lutron Scene."""
    devs = []
    for (keypad, button) in hass.data[LUTRON_DEVICES]['scene']:
        dev = LutronScene(keypad, button)
        devs.append(dev)

    add_devices(devs, True)


class LutronScene(Scene):
    """Representation of a Lutron scene."""

    def __init__(self, keypad, button):
        """Initialize the Lutron scene."""
        self._button = button
        self._keypad = keypad

    @property
    def name(self):
        """Return the name of the scene."""
        return self._button.name

    @property
    def should_poll(self):
        """Return that polling is not necessary."""
        return False

    @property
    def is_on(self):
        """Scene state is not implemented (yet)."""
        return False

    def activate(self, **kwargs):
        """Activate the scene."""
        self._keypad.press(self._button)
