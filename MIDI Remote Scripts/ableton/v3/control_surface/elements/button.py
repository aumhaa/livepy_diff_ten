from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as ButtonElementBase
from .. import MIDI_CC_TYPE

class ButtonElement(ButtonElementBase):

    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, is_momentary=True, led_channel=None, *a, **k):
        self._led_channel = led_channel
        (super().__init__)(is_momentary, msg_type, channel, identifier, *a, **k)

    def send_value(self, value, force=False, channel=None):
        channel = channel if channel is not None else self._led_channel
        super().send_value(value, force=force, channel=channel)