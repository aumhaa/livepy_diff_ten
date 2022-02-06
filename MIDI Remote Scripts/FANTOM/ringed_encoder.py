from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.elements import EncoderElement

class RingedEncoderElement(EncoderElement):

    def is_mapped_manually(self):
        return not self._is_mapped and not self._is_being_forwarded

    def release_parameter(self):
        super().release_parameter()
        if not self.is_mapped_manually():
            if not self._parameter_to_map_to:
                self.send_value(0, force=True)