from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import SysexElement

class OptimizedSysexElement(SysexElement):

    def __init__(self, *a, **k):
        super(OptimizedSysexElement, self).__init__(*a, **k)
        self._last_sent_message = None

    def _do_send_value(self, message):
        if message != self._last_sent_message and self.send_midi(message):
            self._last_sent_message = message


class SkinableSysexElement(OptimizedSysexElement):

    def __init__(self, skin = Skin(), *a, **k):
        super(SkinableSysexElement, self).__init__(*a, **k)
        self._skin = skin

    def set_light(self, value):
        color = self._skin[value]
        color.draw(self)
