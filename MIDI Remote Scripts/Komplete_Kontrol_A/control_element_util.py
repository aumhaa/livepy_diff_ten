from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, midi
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement, SysexElement
from .physical_display_element import PhysicalDisplayElement
from .skin import skin
MIDI_CHANNEL = 15

def create_button(identifier, name):
    return ButtonElement(False, MIDI_CC_TYPE, MIDI_CHANNEL, identifier, name=name, skin=skin)


def create_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, MIDI_CHANNEL, identifier, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=name, encoder_sensitivity=1.0)


def create_display_line(header, line_index, name, width = 0):
    line = PhysicalDisplayElement(width_in_chars=width, name=name)
    line.set_message_parts(header + (line_index,), (midi.SYSEX_END,))
    return line


def create_sysex_element(header, index, name):
    return SysexElement(lambda value: header + (value, index, midi.SYSEX_END), default_value=0, name=name)


def create_display_matrix(num_elements, header, factory, name, **k):
    return ButtonMatrixElement(rows=[[ factory(header, index, u'{}_{}'.format(name, index), **k) for index in xrange(num_elements) ]], name=u'{}s'.format(name))
