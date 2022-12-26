from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listenable_property
from .. import Component
from ..controls import ToggleButtonControl

class AccentComponent(Component):
    accent_button = ToggleButtonControl(toggled_color='Accent.On',
      untoggled_color='Accent.Off')

    @depends(full_velocity=None)
    def __init__(self, name='Accent', full_velocity=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._full_velocity = full_velocity

    @listenable_property
    def activated(self):
        return self._full_velocity.enabled

    @accent_button.toggled
    def accent_button(self, is_toggled, _):
        self._full_velocity.enabled = is_toggled
        self.notify_activated()

    @accent_button.released_delayed
    def accent_button(self, _):
        self.accent_button.is_toggled = False
        self._full_velocity.enabled = False
        self.notify_activated()