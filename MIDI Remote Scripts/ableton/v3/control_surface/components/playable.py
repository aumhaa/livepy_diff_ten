from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as PlayableComponentBase

class PlayableComponent(PlayableComponentBase):

    def __init__(self, is_private=True, *a, **k):
        (super().__init__)(*a, **k)
        self.is_private = is_private
        self._accent_component.is_private = is_private