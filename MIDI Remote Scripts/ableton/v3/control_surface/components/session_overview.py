from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionOverviewComponentBase
from ableton.v3.base import depends

class SessionOverviewComponent(SessionOverviewComponentBase):

    @depends(session_ring=None)
    def __init__(self, name='Session_Overview', session_ring=None, *a, **k):
        (super().__init__)(a, name=name, session_ring=session_ring, enable_skinning=True, **k)