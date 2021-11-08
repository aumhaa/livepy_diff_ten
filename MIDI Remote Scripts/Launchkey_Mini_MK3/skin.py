from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin, merge_skins
from novation.colors import Mono, Rgb
import novation.skin as base_skin

class Colors(object):

    class Recording(object):
        On = Mono.ON
        Off = Mono.OFF

    class TrackNavigation(object):
        On = Mono.HALF
        Pressed = Mono.ON

    class SceneNavigation(object):
        On = Mono.HALF
        Pressed = Mono.ON

    class DrumGroup(object):
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.WHITE
        PadMutedSelected = Rgb.WHITE
        PadSoloedSelected = Rgb.WHITE
        Navigation = Rgb.WHITE_HALF
        NavigationPressed = Rgb.WHITE


skin = merge_skins(base_skin, Skin(Colors)*())