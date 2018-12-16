from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    continue_button = ButtonControl()
    jump_encoder = EncoderControl()
    loop_start_encoder = EncoderControl()

    @continue_button.pressed
    def continue_button(self, _):
        self.song.continue_playing()

    @jump_encoder.value
    def jump_encoder(self, value, _):
        scaled_value = value * 64
        self.song.jump_by(scaled_value * 4.0 if self.song.is_playing else scaled_value)

    @loop_start_encoder.value
    def loop_start_encoder(self, value, _):
        self.song.loop_start = max(0.0, self.song.loop_start + value * 64 * 4.0)

    def _update_stop_button_color(self):
        self._stop_button.color = self._play_toggle.untoggled_color if self._play_toggle.is_toggled else self._play_toggle.toggled_color
