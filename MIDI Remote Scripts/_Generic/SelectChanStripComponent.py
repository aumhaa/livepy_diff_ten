from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ChannelStripComponent import ChannelStripComponent

class SelectChanStripComponent(ChannelStripComponent):
    u""" Subclass of channel strip component that selects tracks that it arms """

    def __init__(self):
        ChannelStripComponent.__init__(self)

    def _arm_value(self, value):
        assert self._arm_button != None
        assert value in range(128)
        if self.is_enabled():
            track_was_armed = False
            if self._track != None and self._track.can_be_armed:
                track_was_armed = self._track.arm
            ChannelStripComponent._arm_value(self, value)
            if self._track != None and self._track.can_be_armed:
                if self._track.arm and not track_was_armed:
                    if self._track.view.select_instrument():
                        self.song().view.selected_track = self._track
