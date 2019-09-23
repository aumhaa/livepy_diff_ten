from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import find_nearest_color, PlayableComponent
from novation.colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE
from novation.drum_group import DrumGroupComponent as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        self._track = None
        self._track_color = 0

    def set_parent_track(self, track):
        self._track = track
        self.__on_track_color_changed.subject = track if liveobj_valid(track) else None
        self.__on_track_color_changed()

    def set_drum_group_device(self, drum_group_device):
        super(DrumGroupComponent, self).set_drum_group_device(drum_group_device)
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if pad else self._track_color
        if color in (u'DrumGroup.PadFilled', u'DrumGroup.PadEmpty') and liveobj_valid(self._track):
            color = self._track_color
        button.color = color

    @listens(u'color')
    def __on_track_color_changed(self):
        self._track_color = 0
        if liveobj_valid(self._track):
            self._track_color = CLIP_COLOR_TABLE.get(self._track.color, None)
            if self._track_color is None:
                self._track_color = find_nearest_color(RGB_COLOR_TABLE, self._track.color)
        self._update_led_feedback()
