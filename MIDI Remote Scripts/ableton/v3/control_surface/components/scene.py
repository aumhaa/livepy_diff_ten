from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import const, depends, listens, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl
from . import ClipSlotComponent

class SceneComponent(Component):
    launch_button = ButtonControl()
    select_button = ButtonControl(color=None)
    delete_button = ButtonControl(color=None)
    duplicate_button = ButtonControl(color=None)

    @depends(session_ring=None, color_for_liveobj_function=(const(None)))
    def __init__(self, session_ring=None, clip_slot_component_type=None, color_for_liveobj_function=None, is_private=True, *a, **k):
        (super().__init__)(*a, **k)
        self.is_private = is_private
        self._color_for_liveobj_function = color_for_liveobj_function
        self._session_ring = session_ring
        self._scene = None
        clip_slot_component_type = clip_slot_component_type or ClipSlotComponent
        self._clip_slots = [clip_slot_component_type(parent=self) for _ in range(session_ring.num_tracks)]
        self.register_slot(session_ring, self._reassign_clip_slots, 'tracks')

    @property
    def scene(self):
        return self._scene

    def set_scene(self, scene):
        if liveobj_changed(scene, self._scene):
            self._scene = scene
            self._SceneComponent__on_is_triggered_changed.subject = scene
            self._SceneComponent__on_scene_color_changed.subject = scene
            self.update()

    def clip_slot(self, index):
        return self._clip_slots[index]

    def set_launch_button(self, button):
        self.launch_button.set_control_element(button)
        self.update()

    def set_select_button(self, button):
        self.select_button.set_control_element(button)

    def set_delete_button(self, button):
        self.delete_button.set_control_element(button)

    def set_duplicate_button(self, button):
        self.duplicate_button.set_control_element(button)

    @launch_button.pressed
    def launch_button(self, _):
        self._on_launch_button_pressed()

    def _on_launch_button_pressed(self):
        if self.select_button.is_pressed:
            self._do_select_scene()
        elif liveobj_valid(self._scene):
            if self.duplicate_button.is_pressed:
                self._do_duplicate_scene()
            elif self.delete_button.is_pressed:
                self._do_delete_scene()
            else:
                self._do_launch_scene(True)
                self._show_launched_scene_as_selected_scene()

    @launch_button.released
    def launch_button(self, _):
        self._on_launch_button_released()

    def _on_launch_button_released(self):
        if liveobj_valid(self._scene):
            if self.launch_button.is_momentary:
                if not self._any_modifier_pressed():
                    self._do_launch_scene(False)

    def _do_launch_scene(self, fire_state):
        self._scene.set_fire_button_state(fire_state)

    def _do_select_scene(self):
        self._select_scene_in_song()

    def _do_delete_scene(self):
        try:
            if liveobj_valid(self._scene):
                song = self.song
                song.delete_scene(list(song.scenes).index(self._scene))
        except RuntimeError:
            pass

    def _do_duplicate_scene(self):
        try:
            song = self.song
            song.duplicate_scene(list(song.scenes).index(self._scene))
        except (Live.Base.LimitationError, IndexError, RuntimeError):
            pass

    def _show_launched_scene_as_selected_scene(self):
        if self.song.select_on_launch:
            self._select_scene_in_song()

    def _select_scene_in_song(self):
        if liveobj_valid(self._scene):
            if liveobj_changed(self.song.view.selected_scene, self._scene):
                self.song.view.selected_scene = self._scene

    def _any_modifier_pressed(self):
        return self.select_button.is_pressed or self.delete_button.is_pressed or self.duplicate_button.is_pressed

    def update(self):
        super().update()
        self._reassign_clip_slots()
        self._update_launch_button_color()

    def _update_launch_button_color(self):
        value_to_send = 'Session.NoScene'
        if liveobj_valid(self._scene):
            value_to_send = self._feedback_value()
        self.launch_button.color = value_to_send

    def _feedback_value(self):
        value = 'Session.Scene'
        if self._scene.is_triggered:
            value = 'Session.SceneTriggered'
        else:
            possible_color = self._idle_color()
            if possible_color:
                value = possible_color
        return value

    def _idle_color(self):
        value = None
        if self._color_for_liveobj_function:
            if liveobj_valid(self._scene):
                value = self._color_for_liveobj_function(self._scene)
        if value is not None:
            return value
        return 'Session.Scene'

    def _reassign_clip_slots(self):
        if liveobj_valid(self._scene) and self.is_enabled():
            scene_offset = list(self.song.scenes).index(self._scene)
            regular_tracks = self.song.tracks
            for slot_wrapper, track in zip(self._clip_slots, self._session_ring.tracks):
                if track in regular_tracks:
                    slot_wrapper.set_clip_slot(track.clip_slots[scene_offset])
                else:
                    slot_wrapper.set_non_player_track(track)

        else:
            for slot in self._clip_slots:
                slot.set_clip_slot(None)

    @listens('is_triggered')
    def __on_is_triggered_changed(self):
        self._update_launch_button_color()

    @listens('color')
    def __on_scene_color_changed(self):
        self._update_launch_button_color()