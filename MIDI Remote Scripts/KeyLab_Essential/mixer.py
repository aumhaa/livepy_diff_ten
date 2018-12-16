from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.components.mixer import simple_track_assigner
from .channel_strip import ChannelStripComponent

class MixerComponent(MixerComponentBase):

    def _create_strip(self):
        return ChannelStripComponent()
