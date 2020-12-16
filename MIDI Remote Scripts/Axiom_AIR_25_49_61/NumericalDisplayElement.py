from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import range
from future.utils import string_types
from past.utils import old_div
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from .NumericalDisplaySegment import NumericalDisplaySegment

class NumericalDisplayElement(PhysicalDisplayElement):
    u""" Special display element that only displays numerical values """
    _ascii_translations = {u'0': 48,
     u'1': 49,
     u'2': 50,
     u'3': 51,
     u'4': 52,
     u'5': 53,
     u'6': 54,
     u'7': 55,
     u'8': 56,
     u'9': 57}

    def __init__(self, width_in_chars, num_segments):
        PhysicalDisplayElement.__init__(self, width_in_chars, num_segments)
        self._logical_segments = []
        self._translation_table = NumericalDisplayElement._ascii_translations
        width_without_delimiters = self._width - num_segments + 1
        width_per_segment = int(old_div(width_without_delimiters, num_segments))
        for index in range(num_segments):
            new_segment = NumericalDisplaySegment(width_per_segment, self.update)
            self._logical_segments.append(new_segment)

    def display_message(self, message):
        assert self._message_header != None
        assert message != None
        assert isinstance(message, string_types)
        if not self._block_messages:
            message = NumericalDisplaySegment.adjust_string(message, self._width)
            self.send_midi(self._message_header + tuple([ self._translate_char(c) for c in message ]) + self._message_tail)

    def _translate_char(self, char_to_translate):
        assert char_to_translate != None
        assert isinstance(char_to_translate, string_types)
        assert len(char_to_translate) == 1
        if char_to_translate in list(self._translation_table.keys()):
            result = self._translation_table[char_to_translate]
        else:
            result = self._translation_table[u'0']
        return result
