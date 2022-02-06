from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as EncoderElementBase
from ableton.v2.control_surface.elements.encoder import _map_modes
from .. import MIDI_CC_TYPE

class EncoderElement(EncoderElementBase):

    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, map_mode=_map_modes.absolute, needs_takeover=True, *a, **k):
        (super().__init__)(msg_type, channel, identifier, map_mode, *a, **k)
        self.set_needs_takeover(needs_takeover)