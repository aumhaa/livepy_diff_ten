from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionNavigationComponentBase
from .util import skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        (super(SessionNavigationComponent, self).__init__)(*a, **k)
        skin_scroll_buttons(self._vertical_banking, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_banking, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._vertical_paginator, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_paginator, 'Session.Navigation', 'Session.NavigationPressed')