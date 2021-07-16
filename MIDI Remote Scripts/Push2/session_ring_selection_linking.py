from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface as SessionRingSelectionLinkingBase

class SessionRingSelectionLinking(SessionRingSelectionLinkingBase):

    def _current_track(self):
        return self._session_ring.selected_item