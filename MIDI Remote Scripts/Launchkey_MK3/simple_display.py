from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import task
from ableton.v2.control_surface import NotifyingControlElement
from ableton.v3.base import as_ascii, get_default_ascii_translations
NON_ASCII_ENCODING = 17
TRANSLATED_DEGREE_SYMBOL = 48
ascii_translations = get_default_ascii_translations()
ascii_translations['°'] = (NON_ASCII_ENCODING, TRANSLATED_DEGREE_SYMBOL)
as_ascii = partial(as_ascii, ascii_translations=ascii_translations)

class SimpleDisplayElement(NotifyingControlElement):

    def __init__(self, header, tail, *a, **k):
        (super(SimpleDisplayElement, self).__init__)(*a, **k)
        self._message_header = header
        self._message_tail = tail
        self._message_to_send = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def display_message(self, message):
        if message:
            self._message_to_send = self._message_header + tuple(as_ascii(message)) + self._message_tail
            self._request_send_message()

    def update(self):
        self._last_sent_message = None
        self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        self.display_message(' ')

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            NotifyingControlElement.send_midi(self, midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if self._message_to_send:
            self.send_midi(self._message_to_send)