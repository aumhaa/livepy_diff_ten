from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Dependency import depends
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.EncoderElement import EncoderElement

@depends(skin=None)
def make_button(identifier, name, skin = None):
    return ButtonElement(True, MIDI_NOTE_TYPE, 0, identifier, name=name, skin=skin)


def make_slider(identifier, name):
    return SliderElement(MIDI_CC_TYPE, 0, identifier, name=name)


def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, map_mode=Live.MidiMap.MapMode.absolute, name=name)


def make_button_row(identifier_sequence, element_factory, name):
    return ButtonMatrixElement(rows=[ [element_factory(identifier, name + u'_%d' % index)] for index, identifier in enumerate(identifier_sequence) ])
