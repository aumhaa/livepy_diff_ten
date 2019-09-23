from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, SysexElement
from . import sysex
SESSION_WIDTH = 8
SESSION_HEIGHT = 8

@depends(skin=None)
def create_button(identifier, name, msg_type = MIDI_CC_TYPE, channel = 0, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


class LaunchpadElements(object):
    model_id = 0
    default_layout = 0

    def __init__(self, *a, **k):
        super(LaunchpadElements, self).__init__(*a, **k)
        self.up_button = create_button(91, u'Up_Button')
        self.down_button = create_button(92, u'Down_Button')
        self.left_button = create_button(93, u'Left_Button')
        self.right_button = create_button(94, u'Right_Button')
        self.session_mode_button = create_button(95, u'Session_Mode_Button')
        self.scene_launch_buttons_raw = [ create_button(identifier, u'Scene_Launch_Button_{}'.format(row_index)) for row_index, identifier in enumerate(xrange(89, 18, -10)) ]
        self.scene_launch_buttons = ButtonMatrixElement(rows=[self.scene_launch_buttons_raw], name=u'Scene_Launch_Buttons')
        self.clip_launch_matrix = ButtonMatrixElement(rows=[ [ create_button(offset + col_index, u'{}_Clip_Launch_Button_{}'.format(col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in xrange(SESSION_WIDTH) ] for row_index, offset in enumerate(xrange(81, 10, -10)) ], name=u'Clip_Launch_Matrix')
        self.firmware_mode_switch = SysexElement(name=u'Firmware_Mode_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (self.model_id,
         sysex.FIRMWARE_MODE_COMMAND_BYTE,
         v,
         sysex.SYSEX_END_BYTE), default_value=sysex.STANDALONE_MODE_BYTE, optimized=True)
        layout_switch_identifier = sysex.STD_MSG_HEADER + (self.model_id, sysex.LAYOUT_COMMAND_BYTE)
        self.layout_switch = SysexElement(name=u'Layout_Switch', sysex_identifier=layout_switch_identifier, send_message_generator=lambda v: layout_switch_identifier + (v, sysex.SYSEX_END_BYTE), default_value=self.default_layout)
