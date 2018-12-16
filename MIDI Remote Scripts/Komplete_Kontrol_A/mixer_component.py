from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from .channel_strip_component import ChannelStripComponent

class MixerComponent(MixerComponentBase):

    def set_mute_button(self, button):
        self._selected_strip.set_mute_button(button)

    def set_solo_button(self, button):
        self._selected_strip.set_solo_button(button)

    def set_track_name_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_name_data_source(),))

    def set_track_volume_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_volume_data_source,))

    def set_track_panning_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            display.set_data_sources((strip.track_panning_data_source,))

    def set_track_type_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            strip.track_type_display.set_control_element(display)

    def set_track_mute_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            strip.track_mute_display.set_control_element(display)

    def set_track_solo_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            strip.track_solo_display.set_control_element(display)

    def set_track_selection_displays(self, displays):
        for strip, display in izip_longest(self._channel_strips, displays or []):
            strip.track_selection_display.set_control_element(display)

    def _create_strip(self):
        return ChannelStripComponent(parent=self)
