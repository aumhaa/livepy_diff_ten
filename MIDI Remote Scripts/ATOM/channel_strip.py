from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
import ableton.v2.control_surface.components as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):
    empty_color = 'Mixer.EmptyTrack'

    def _update_select_button(self):
        if liveobj_valid(self._track) and self.song.view.selected_track == self._track:
            self.select_button.color = 'Mixer.Selected'
        else:
            self.select_button.color = 'DefaultButton.Off'