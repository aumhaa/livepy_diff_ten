from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SysexValueControl import SysexValueControl

class ButtonSysexControl(SysexValueControl):
    u"""
    A SysexValueControl that behaves like a button so it can be used as a mode button of
    the ModesComponent.
    """

    def set_light(self, value):
        pass

    def is_momentary(self):
        return False
