from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
from ableton.v2.control_surface.components import BackgroundComponent as BackgroundComponentBase

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        super(BackgroundComponent, self)._clear_control(name, control)
        if control:
            self._control_slots[name] = self.register_slot(control, nop, u'value')
