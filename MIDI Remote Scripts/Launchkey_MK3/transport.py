from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import ButtonControl
import novation.transport as TransportComponentBase

class TransportComponent(TransportComponentBase):
    alt_stop_button = ButtonControl()

    @alt_stop_button.pressed
    def alt_stop_button(self, _):
        self.song.is_playing = False