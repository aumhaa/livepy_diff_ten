from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionNavigationComponentBase
from .scroll import ScrollComponent

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        (super(SessionNavigationComponent, self).__init__)(*a, **k)
        self._horizontal_paginator = ScrollComponent((self.track_pager_type(self._session_ring)),
          parent=self)