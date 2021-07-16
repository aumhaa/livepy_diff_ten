from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color

class Basic:
    OFF = Color(0)
    ON = Color(1)
    DISABLED = Color(2)


class Rgb:
    YELLOW = Color(3)
    LIGHT_BLUE = Color(6)
    RED = Color(13)
    ORANGE = Color(14)
    GREEN = Color(4)
    DARK_BLUE = Color(63)