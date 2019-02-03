from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    continue_button = ButtonControl()
    jump_encoder = EncoderControl()
    loop_start_encoder = EncoderControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.__on_signature_numerator_changed.subject = self.song
        self.__on_signature_denominator_changed.subject = self.song
        self._calculate_distance_to_move()

    @continue_button.pressed
    def continue_button(self, _):
        self.song.continue_playing()

    @jump_encoder.value
    def jump_encoder(self, value, _):
        self.song.jump_by(value * self._distance_to_move)

    @loop_start_encoder.value
    def loop_start_encoder(self, value, _):
        self.song.loop_start = max(0.0, self.song.loop_start + value * self._distance_to_move)

    @listens(u'signature_numerator')
    def __on_signature_numerator_changed(self):
        self._calculate_distance_to_move()

    @listens(u'signature_denominator')
    def __on_signature_denominator_changed(self):
        self._calculate_distance_to_move()

    def _calculate_distance_to_move(self):
        self._distance_to_move = 4.0 / self.song.signature_denominator * self.song.signature_numerator * 64

    def _update_stop_button_color(self):
        self._stop_button.color = self._play_toggle.untoggled_color if self._play_toggle.is_toggled else self._play_toggle.toggled_color
