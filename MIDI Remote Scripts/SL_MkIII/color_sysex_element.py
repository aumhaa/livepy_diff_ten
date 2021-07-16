from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
import ableton.v2.control_surface.elements as ColorSysexElementBase

class ColorSysexElement(ColorSysexElementBase):

    class ProxiedInterface(ColorSysexElementBase.ProxiedInterface):
        set_light = nop