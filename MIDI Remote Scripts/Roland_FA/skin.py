from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color
from ableton.v2.control_surface import Skin

class Colors:

    class DefaultButton:
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

    class Transport:
        PlayOn = Color(127)
        PlayOff = Color(0)

    class Recording:
        On = Color(127)
        Off = Color(0)


def make_default_skin():
    return Skin(Colors)
