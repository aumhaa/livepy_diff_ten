from __future__ import absolute_import, print_function, unicode_literals
from novation import sysex
from novation.launchpad_elements import create_button, LaunchpadElements
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_MINI_MK3_ID
    default_layout = sysex.KEYS_LAYOUT_BYTE

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.drums_mode_button = create_button(96, u'Drums_Mode_Button')
        self.keys_mode_button = create_button(97, u'Keys_Mode_Button')
        self.user_mode_button = create_button(98, u'User_Mode_Button')
