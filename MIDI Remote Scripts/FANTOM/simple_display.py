from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import task
from ableton.v2.control_surface import NotifyingControlElement
from ableton.v2.control_surface.elements import adjust_string
QUESTION_MARK = 63

def as_ascii(data):
    result = []
    for char in data:
        ascii = ord(char)
        if ascii > 127:
            ascii = QUESTION_MARK
        else:
            result.append(ascii)

    return result


class SimpleDisplayElement(NotifyingControlElement):

    def __init__(self, header, tail, max_chars=6, *a, **k):
        (super(SimpleDisplayElement, self).__init__)(*a, **k)
        self._max_chars = max_chars
        self._message_header = header
        self._message_tail = tail
        self._message_to_send = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def display_data(self, data):
        self._message_to_send = self._message_header + tuple(as_ascii(adjust_string(data, self._max_chars).strip())) + self._message_tail
        self._request_send_message()

    def update(self):
        self._last_sent_message = None
        self._request_send_message()

    def clear_send_cache(self):
        self._last_sent_message = None
        self._request_send_message()

    def reset(self):
        self.display_data('')

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            NotifyingControlElement.send_midi(self, midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self):
        if self._message_to_send:
            self.send_midi(self._message_to_send)