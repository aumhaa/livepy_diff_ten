from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase

class MixerComponent(MixerComponentBase):

    def set_static_color_value(self, value):
        for strip in self._channel_strips:
            strip.set_static_color_value(value)

    def set_static_color_controls(self, controls):
        for strip, control in izip_longest(self._channel_strips, controls or []):
            strip.static_color_control.set_control_element(control)

    def set_track_color_controls(self, controls):
        for strip, control in izip_longest(self._channel_strips, controls or []):
            strip.track_color_control.set_control_element(control)

    def set_send_a_controls(self, controls):
        self._set_send_controls(controls, 0)

    def set_send_b_controls(self, controls):
        self._set_send_controls(controls, 1)

    def _set_send_controls(self, controls, send_index):
        if controls:
            for index, control in enumerate(controls):
                if control:
                    self.channel_strip(index).set_send_controls((None,) * send_index + (control,))

        else:
            for strip in self._channel_strips:
                strip.set_send_controls(None)
