from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import merge_skins, Skin
from ableton.v2.control_surface.elements import Color
from novation.colors import Rgb
from novation.skin import skin as base_skin

class Colors:

    class Mode:

        class Launch:
            On = Color((Rgb.PALE_GREEN_HALF.midi_value, Rgb.WHITE_HALF.midi_value))
            Off = Color((Rgb.CREAM.midi_value, Rgb.WHITE_HALF.midi_value))


skin = merge_skins(*(base_skin, Skin(Colors)))
