from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color

class Colors(object):

    class DefaultButton(object):
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

    class Transport(object):
        PlayOn = Color(127)
        PlayOff = Color(0)

    class Recording(object):
        On = Color(127)
        Off = Color(0)


def make_default_skin():
    return Skin(Colors)