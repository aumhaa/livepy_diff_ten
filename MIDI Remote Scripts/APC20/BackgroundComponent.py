from __future__ import absolute_import, print_function, unicode_literals
import _Framework.BackgroundComponent as BackgroundComponentBase
from _Framework.Util import nop

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        if control:
            control.add_value_listener(nop)
        elif name in self._control_map:
            self._control_map[name].remove_value_listener(nop)
        super(BackgroundComponent, self)._clear_control(name, control)