from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.components import find_nearest_color
from ableton.v2.control_surface.control import SendValueControl
from .colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE

class ChannelStripComponent(ChannelStripComponentBase):
    empty_color = u'Mixer.EmptyTrack'
    track_color_control = SendValueControl()
    static_color_control = SendValueControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._static_color_value = 0

    def set_static_color_value(self, value):
        self._static_color_value = value
        self._update_static_color_control()

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self.__on_track_color_changed.subject = track if liveobj_valid(track) else None
        self._update_track_color_control()
        self._update_static_color_control()

    @listens(u'color')
    def __on_track_color_changed(self):
        self._update_track_color_control()

    def _update_track_color_control(self, *a):
        value = 0
        if liveobj_valid(self._track):
            value = CLIP_COLOR_TABLE.get(self._track.color, None)
            if value is None:
                value = find_nearest_color(RGB_COLOR_TABLE, self._track.color)
        self.track_color_control.value = value

    def _update_static_color_control(self):
        self.static_color_control.value = self._static_color_value if liveobj_valid(self._track) else 0
