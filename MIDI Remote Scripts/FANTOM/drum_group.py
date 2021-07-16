from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
import ableton.v2.control_surface.components as DrumGroupComponentBase
from ableton.v2.control_surface.components import PlayableComponent

class DrumGroupComponent(DrumGroupComponentBase):

    def set_drum_group_device(self, drum_group_device):
        super(DrumGroupComponent, self).set_drum_group_device(drum_group_device)
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        button.color = self._color_for_pad(pad) if pad else 'DrumGroup.PadEmpty'