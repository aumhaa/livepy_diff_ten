from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from .channel_strip import ChannelStripComponent

class MixerComponent(MixerComponentBase):

    def _create_strip(self):
        return ChannelStripComponent()
