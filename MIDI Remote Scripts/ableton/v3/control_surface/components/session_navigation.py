from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionNavigationComponentBase
from ...base import add_scroll_encoder, depends, skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    @depends(session_ring=None)
    def __init__(self, name='Session_Navigation', session_ring=None, is_private=True, *a, **k):
        (super().__init__)(a, name=name, session_ring=session_ring, **k)
        self.is_private = is_private
        add_scroll_encoder(self._horizontal_banking)
        add_scroll_encoder(self._vertical_banking)
        for c in (
         self._vertical_banking,
         self._horizontal_banking,
         self._vertical_paginator,
         self._horizontal_paginator):
            skin_scroll_buttons(c, 'Session.Navigation', 'Session.NavigationPressed')

    def set_horizontal_encoder(self, control):
        self._horizontal_banking.scroll_encoder.set_control_element(control)

    def set_vertical_encoder(self, control):
        self._vertical_banking.scroll_encoder.set_control_element(control)