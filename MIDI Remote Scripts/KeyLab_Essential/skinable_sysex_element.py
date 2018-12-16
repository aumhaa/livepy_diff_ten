from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import SysexElement

class SkinableSysexElement(SysexElement):

    def __init__(self, skin = Skin(), *a, **k):
        super(SkinableSysexElement, self).__init__(*a, **k)
        self._skin = skin

    def set_light(self, value):
        color = self._skin[value]
        color.draw(self)
