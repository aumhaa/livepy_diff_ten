from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as SysexElementBase

class SysexElement(SysexElementBase):

    def __init__(self, use_first_byte_as_value=False, *a, **k):
        (super().__init__)(*a, **k)
        self._use_first_byte_as_value = use_first_byte_as_value

    def receive_value(self, value):
        if self._use_first_byte_as_value:
            value = value[0]
        super().receive_value(value)