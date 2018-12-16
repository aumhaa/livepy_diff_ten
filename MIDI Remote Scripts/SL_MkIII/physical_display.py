from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, ifilter, imap
from ableton.v2.base import first
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase
from .sysex import TEXT_PROPERTY_BYTE

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _translate_string(self, string):
        return map(self._translate_char, ifilter(lambda c: c in self._translation_table, string))


class ConfigurablePhysicalDisplayElement(PhysicalDisplayElement):

    def __init__(self, v_position = 0, *a, **k):
        super(ConfigurablePhysicalDisplayElement, self).__init__(*a, **k)
        self._v_position = v_position

    def _build_display_message(self, display):

        def wrap_segment_message(segment):
            return chain(segment.position_identifier(), (TEXT_PROPERTY_BYTE, self._v_position), self._translate_string(unicode(segment).strip()), (0,))

        return chain(*imap(wrap_segment_message, display._logical_segments))


class SpecialPhysicalDisplayElement(PhysicalDisplayElement):

    def _send_message(self):
        if self._message_to_send is None:
            self._message_to_send = self._build_message(map(first, self._central_resource.owners))
        inner_message = self._message_to_send[len(self._message_header):-len(self._message_tail)]
        if not self._is_whitespace(inner_message):
            self.send_midi(self._message_to_send)

    def _is_whitespace(self, message):
        return all(map(lambda c: c == self.ascii_translations[u' '], message))
