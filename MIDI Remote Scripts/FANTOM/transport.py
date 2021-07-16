from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, listens
import ableton.v2.control_surface.components as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl
from .control import DisplayControl
MAX_NUM_BARS_WITH_BEATS = 9999

class TransportComponent(TransportComponentBase):
    capture_midi_button = ButtonControl()
    tempo_coarse_control = EncoderControl()
    tempo_fine_control = EncoderControl()
    beat_time_display = DisplayControl()
    tempo_display = DisplayControl()

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._TransportComponent__on_song_time_changed.subject = self.song
        self._TransportComponent__on_tempo_changed.subject = self.song
        self._TransportComponent__on_can_capture_midi_changed.subject = self.song
        self._TransportComponent__on_can_capture_midi_changed()

    def set_tempo_fine_control(self, control):
        self.tempo_fine_control.set_control_element(control)

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @tempo_coarse_control.value
    def tempo_coarse_control(self, value, _):
        factor = 1 if value > 0 else -1
        self.song.tempo = clamp(self.song.tempo + factor, 20, 999)

    @tempo_fine_control.value
    def tempo_fine_control(self, value, _):
        factor = 0.1 if value > 0 else -0.1
        self.song.tempo = clamp(self.song.tempo + factor, 20, 999)

    def update(self):
        super(TransportComponent, self).update()
        self._TransportComponent__on_song_time_changed()
        self._TransportComponent__on_tempo_changed()

    @listens('current_song_time')
    def __on_song_time_changed(self):
        beat_time = self.song.get_current_beats_song_time()
        bars = beat_time.bars
        if bars <= MAX_NUM_BARS_WITH_BEATS:
            self.beat_time_display.data = '{}.{}'.format(bars, beat_time.beats)
        else:
            self.beat_time_display.data = str(bars)

    @listens('tempo')
    def __on_tempo_changed(self):
        tempo = '{:.2f}'.format(self.song.tempo)
        self.tempo_display.data = tempo

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.color = 'Transport.Capture{}'.format('On' if self.song.can_capture_midi else 'Off')