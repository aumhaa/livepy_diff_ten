from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from .channel_strip import ChannelStripComponent

class MixerComponent(MixerComponentBase):

    def set_selected_track_name_display(self, display):
        self._selected_strip.set_track_name_display(display)

    def _update_selected_strip(self):
        selected_strip = self._selected_strip
        if liveobj_valid(selected_strip):
            selected_strip.set_track(self.song.view.selected_track)

    def _create_strip(self):
        return ChannelStripComponent()
