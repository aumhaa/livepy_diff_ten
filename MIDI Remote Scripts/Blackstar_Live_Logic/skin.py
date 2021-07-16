from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
LED_ON = Color(127)
LED_OFF = Color(0)

class Colors:

    class DefaultButton:
        On = LED_ON
        Off = LED_OFF
        Disabled = LED_OFF


skin = Skin(Colors)