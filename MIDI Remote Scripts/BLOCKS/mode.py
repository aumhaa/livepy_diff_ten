from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import ButtonControl
import ableton.v2.control_surface.mode as ModesComponentBase

class ModesComponent(ModesComponentBase):
    cycle_mode_button = ButtonControl()

    @cycle_mode_button.pressed
    def cycle_mode_button(self, button):
        if len(self._mode_list):
            self.cycle_mode(1)