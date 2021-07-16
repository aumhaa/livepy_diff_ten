from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface.control import PlayableControl

class NotePadMixin(object):

    def set_matrix(self, matrix):
        super(NotePadMixin, self).set_matrix(matrix)
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.playable_and_listenable)
            button.pressed_color = 'NotePad.Pressed'

    def _on_matrix_pressed(self, _):
        pass

    def _on_matrix_released(self, button):
        self._update_button_color(button)