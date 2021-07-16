from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, starmap
from ableton.v2.base import clamp, group
import ableton.v2.control_surface.elements as PhysicalDisplayElementBase

def message_length(message):
    length = len(message)
    return (
     clamp(length // 128, 0, 127), length % 128)


class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        message_string = display.display_string.strip()
        return chain(message_length(message_string), self._translate_string(message_string))