from __future__ import absolute_import, print_function, unicode_literals
from functools import reduce
from operator import add
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.elements import ButtonMatrixElement, ColorSysexElement, SliderElement, SysexElement
from novation import sysex
from novation.launchpad_elements import create_button, LaunchpadElements, SESSION_WIDTH
from . import sysex_ids as ids
BUTTON_FADER_MAIN_MIDI_CHANNEL = 4
BUTTON_FADER_COLOR_MIDI_CHANNEL = 5
BUTTON_FADER_CC_OFFSET = 21

def create_slider(identifier, name, **k):
    slider = SliderElement(MIDI_CC_TYPE, BUTTON_FADER_MAIN_MIDI_CHANNEL, identifier, name=name, **k)
    slider.set_needs_takeover(False)
    return slider


def button_fader_setup_message_generator(orientation, polarity):
    return sysex.STD_MSG_HEADER + (ids.LP_X_ID,
     sysex.FADER_COMMAND_BYTE,
     0,
     orientation) + reduce(add, [ (index,
     polarity,
     index + BUTTON_FADER_CC_OFFSET,
     0) for index in xrange(SESSION_WIDTH) ]) + (sysex.SYSEX_END_BYTE,)


class Elements(LaunchpadElements):
    model_id = ids.LP_X_ID
    default_layout = sysex.NOTE_LAYOUT_BYTE

    @depends(skin=None)
    def __init__(self, skin = None, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.note_mode_button = create_button(96, u'Note_Mode_Button')
        self.custom_mode_button = create_button(97, u'Custom_Mode_Button')
        self.record_button = create_button(98, u'Record_Button')
        drum_pad_rows = ((64, 65, 66, 67, 96, 97, 98, 99),
         (60, 61, 62, 63, 92, 93, 94, 95),
         (56, 57, 58, 59, 88, 89, 90, 91),
         (52, 53, 54, 55, 84, 85, 86, 87),
         (48, 49, 50, 51, 80, 81, 82, 83),
         (44, 45, 46, 47, 76, 77, 78, 79),
         (40, 41, 42, 43, 72, 73, 74, 75),
         (36, 37, 38, 39, 68, 69, 70, 71))
        self.drum_pads = ButtonMatrixElement(rows=[ [ create_button(row_identifiers[col_index], u'Drum_Pad_{}_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=8) for col_index in xrange(SESSION_WIDTH) ] for row_index, row_identifiers in enumerate(drum_pad_rows) ], name=u'Drum_Pads')
        self.scale_pads = ButtonMatrixElement(rows=[[ create_button(identifier, u'Scale_Pad_{}'.format(identifier), msg_type=MIDI_NOTE_TYPE, channel=15) for identifier in xrange(128) ]], name=u'Scale_Pads')
        self.button_faders = ButtonMatrixElement(rows=[[ create_slider(index + BUTTON_FADER_CC_OFFSET, u'Button_Fader_{}'.format(index)) for index in xrange(SESSION_WIDTH) ]], name=u'Button_Faders')
        self.button_fader_color_elements_raw = [ create_button(index + BUTTON_FADER_CC_OFFSET, u'Button_Fader_Color_Element_{}'.format(index), channel=BUTTON_FADER_COLOR_MIDI_CHANNEL) for index in xrange(SESSION_WIDTH) ]
        self.button_fader_color_elements = ButtonMatrixElement(rows=[self.button_fader_color_elements_raw], name=u'Button_Fader_Color_Elements')
        self.note_layout_switch = SysexElement(name=u'Note_Layout_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (ids.LP_X_ID,
         sysex.NOTE_LAYOUT_COMMAND_BYTE,
         v,
         sysex.SYSEX_END_BYTE), default_value=sysex.SCALE_LAYOUT_BYTE)
        self.scale_feedback_switch = SysexElement(name=u'Scale_Feedback_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (ids.LP_X_ID,
         sysex.SCALE_FEEDBACK_COMMAND_BYTE,
         v,
         sysex.SYSEX_END_BYTE))
        session_button_color_identifier = sysex.STD_MSG_HEADER + (ids.LP_X_ID, 20)
        self.session_button_color_element = ColorSysexElement(name=u'Session_Button_Color_Element', sysex_identifier=session_button_color_identifier, send_message_generator=lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,), skin=skin)
        self.button_fader_setup_element = SysexElement(name=u'Button_Fader_Setup_Element', send_message_generator=button_fader_setup_message_generator)
