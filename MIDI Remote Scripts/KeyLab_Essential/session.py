from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, product
from ableton.v2.control_surface.components import SceneComponent as SceneComponentBase, SessionComponent as SessionComponentBase
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent

    def __init__(self, *a, **k):
        super(SessionComponent, self).__init__(*a, **k)
        self._on_selected_scene_changed.subject = self.song.view
        self._on_selected_scene_changed()

    def set_clip_slot_leds(self, leds):
        assert not leds or leds.width() == self._session_ring.num_tracks and leds.height() == self._session_ring.num_scenes
        if leds:
            for led, (x, y) in leds.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(led)

        else:
            for x, y in product(xrange(self._session_ring.num_tracks), xrange(self._session_ring.num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_led(None)

    @listens(u'selected_scene')
    def _on_selected_scene_changed(self):
        selected_scene_index = list(self.song.scenes).index(self.song.view.selected_scene)
        self._session_ring.set_offsets(self._session_ring.track_offset, selected_scene_index)
