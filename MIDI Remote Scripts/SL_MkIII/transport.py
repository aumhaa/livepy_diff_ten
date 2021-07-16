from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._loop_toggle.view_transform = lambda v: 'Transport.LoopOn' if v else 'Transport.LoopOff'
        self._record_toggle.view_transform = lambda v: 'Recording.On' if v else 'Recording.Off'

    def set_seek_forward_button(self, ffwd_button):
        super(TransportComponent, self).set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super(TransportComponent, self).set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._update_seek_button(self._rwd_button)

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self._update_continue_playing_button()

    def _update_continue_playing_button(self):
        self.continue_playing_button.color = 'Transport.PlayOn' if self.song.is_playing else 'Transport.PlayOff'

    def _update_seek_button(self, button):
        if self.is_enabled():
            if button != None:
                button.set_light('Transport.SeekOn' if button.is_pressed() else 'Transport.SeekOff')

    def _update_stop_button_color(self):
        self.stop_button.color = 'Transport.StopEnabled' if self.play_button.is_toggled else 'Transport.StopDisabled'