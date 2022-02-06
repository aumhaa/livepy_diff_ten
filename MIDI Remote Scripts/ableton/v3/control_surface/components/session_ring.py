from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionRingComponentBase
from ...base import depends

class SessionRingComponent(SessionRingComponentBase):

    @depends(song=None)
    def __init__(self, name='Session_Ring', include_returns=False, tracks_to_use=None, song=None, *a, **k):
        if tracks_to_use is None:
            if include_returns:
                tracks_to_use = lambda: tuple(song.visible_tracks) + tuple(song.return_tracks)
        (super().__init__)(a, name=name, song=song, tracks_to_use=tracks_to_use, **k)