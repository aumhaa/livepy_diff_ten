from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from .skin import skin
MIDI_CHANNEL = 0
SESSION_WIDTH = 8
SESSION_HEIGHT = 2

def create_button(identifier, name, msg_type=MIDI_CC_TYPE, is_momentary=True, **k):
    return ButtonElement(
 is_momentary, msg_type, MIDI_CHANNEL, identifier, name=name, skin=skin, **k)


def create_encoder(identifier, name, map_mode=Live.MidiMap.MapMode.absolute, **k):
    return EncoderElement(
 MIDI_CC_TYPE, MIDI_CHANNEL, identifier, map_mode, name=name, **k)


class Elements(object):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.encoder_push_button = create_button(102, 'Encoder_Push_Button')
        self.back_button = create_button(104, 'Back_Button')
        self.bank_left_button = create_button(110, 'Bank_Left_Button')
        self.bank_right_button = create_button(111, 'Bank_Right_Button')
        self.loop_button = create_button(114, 'Loop_Button')
        self.rewind_button = create_button(115, 'Rewind_Button')
        self.fastforward_button = create_button(116, 'Fastforward_Button')
        self.stop_button = create_button(117, 'Stop_Button')
        self.play_button = create_button(118, 'Play_Button')
        self.record_button = create_button(119, 'Record_Button')
        self.fader_buttons = ButtonMatrixElement(rows=[
         [create_button((index + 32), ('Fader_Button_{}'.format(index)), is_momentary=False) for index in range(SESSION_WIDTH)]],
          name='Fader_Buttons')
        self.scene_launch_buttons = ButtonMatrixElement(rows=[
         [create_button(index + 107, 'Scene_Launch_Button_{}'.format(index)) for index in range(SESSION_HEIGHT)]],
          name='Scene_Launch_Buttons')
        pad_ids = ((40, 41, 42, 43, 48, 49, 50, 51), (36, 37, 38, 39, 44, 45, 46, 47))
        self.pads = ButtonMatrixElement(rows=[[create_button(ident, ('{}_Pad_{}'.format(row_index, ident % SESSION_WIDTH)), msg_type=MIDI_NOTE_TYPE) for ident in pad_ids[row_index]] for row_index in range(SESSION_HEIGHT)],
          name='Pads')
        self.encoder = create_encoder(103,
          'Encoder', map_mode=(Live.MidiMap.MapMode.relative_signed_bit))
        self.master_fader = create_encoder(41, 'Master_Fader')
        self.faders = ButtonMatrixElement(rows=[
         [create_encoder(index + 12, 'Fader_{}'.format(index)) for index in range(SESSION_WIDTH)]],
          name='Faders')
        self.knobs = ButtonMatrixElement(rows=[
         [create_encoder(index + 22, 'Knob_{}'.format(index)) for index in range(8)]],
          name='Knobs')