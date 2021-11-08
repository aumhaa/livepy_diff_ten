from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, object
from .sysex import NUM_SET_PROPERTY_HEADER_BYTES

class MidiMessageCache(object):

    def __init__(self, *a, **k):
        (super(MidiMessageCache, self).__init__)(*a, **k)
        self._messages = []

    def __call__(self, message):
        self._messages = list(filter(lambda m: m[:NUM_SET_PROPERTY_HEADER_BYTES] != message[:NUM_SET_PROPERTY_HEADER_BYTES], self._messages))
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages

    def clear(self):
        self._messages = []