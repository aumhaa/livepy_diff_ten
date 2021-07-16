from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import InputControl
import ableton.v2.control_surface.mode as ModesComponentBase

class ModesComponent(ModesComponentBase):
    __events__ = ('mode_byte', )
    mode_selection_control = InputControl()

    @mode_selection_control.value
    def mode_selection_control(self, value, _):
        modes = self.modes
        if value < len(modes):
            self.selected_mode = modes[value]
            self.notify_mode_byte(value)