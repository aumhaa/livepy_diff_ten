from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import clamp, move_current_song_time
import ableton.v3.control_surface.components as TransportComponentBase
from ableton.v3.control_surface.controls import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    shift_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        factor = 1 if value > 0 else -1
        if self.shift_button.is_pressed:
            self.song.tempo = clamp(self.song.tempo + factor, 20, 999)
        else:
            move_current_song_time(self.song, factor)