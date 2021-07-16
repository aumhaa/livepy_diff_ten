from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import in_range
import ableton.v2.control_surface.elements as ButtonElementBase

class ButtonElement(ButtonElementBase):

    def set_light(self, value):
        if isinstance(value, int) and in_range(value, 0, 128):
            self.send_value(value)
        else:
            super(ButtonElement, self).set_light(value)