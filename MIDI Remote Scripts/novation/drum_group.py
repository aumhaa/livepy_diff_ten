from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as DrumGroupComponentBase
from .util import skin_scroll_buttons

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        (super(DrumGroupComponent, self).__init__)(*a, **k)
        skin_scroll_buttons(self._position_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')
        skin_scroll_buttons(self._page_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')

    def set_parent_track(self, track):
        pass