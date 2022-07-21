from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as ClipSlotComponentBase
import ableton.v2.control_surface.components as SceneComponentBase
import ableton.v2.control_surface.components as SessionComponentBase
from ...base import depends, liveobj_valid
from ..controls import ButtonControl, control_list

class ClipSlotComponent(ClipSlotComponentBase):

    def __init__(self, color_for_obj_function=None, is_private=True, *a, **k):
        self._color_for_obj_function = color_for_obj_function
        (super().__init__)(*a, **k)
        self.is_private = is_private
        self._record_button_color = 'Session.ClipRecordButton'

    @property
    def clip_slot(self):
        return self._clip_slot

    def _color_value(self, slot_or_clip):
        if self._color_for_obj_function:
            if liveobj_valid(slot_or_clip):
                return self._color_for_obj_function(slot_or_clip)
        return super()._color_value(slot_or_clip)


class SceneComponent(SceneComponentBase):

    def __init__(self, clip_slot_component_type=None, color_for_obj_function=None, is_private=True, *a, **k):
        self._color_for_obj_function = color_for_obj_function
        clip_slot_component_type = clip_slot_component_type or ClipSlotComponent
        self._create_clip_slot = lambda: clip_slot_component_type(parent=self,
          color_for_obj_function=color_for_obj_function)
        (super().__init__)(*a, **k)
        self.is_private = is_private
        self._no_scene_color = 'Session.SceneEmpty'

    @property
    def scene(self):
        return self._scene

    def _color_value(self, color):
        if self._color_for_obj_function:
            if liveobj_valid(self._scene):
                return self._color_for_obj_function(self._scene)
        return super()._color_value(color)


class SessionComponent(SessionComponentBase):
    stop_all_clips_button = ButtonControl(color='Session.StopAllClips',
      pressed_color='Session.StopAllClipsPressed')
    stop_track_clip_buttons = control_list(ButtonControl)

    @depends(session_ring=None)
    def __init__(self, name='Session', session_ring=None, scene_component_type=None, clip_slot_component_type=None, color_for_obj_function=None, is_private=True, *a, **k):
        scene_component_type = scene_component_type or SceneComponent
        self._create_scene = lambda: scene_component_type(parent=self,
          session_ring=(self._session_ring),
          clip_slot_component_type=clip_slot_component_type,
          color_for_obj_function=color_for_obj_function)
        (super().__init__)(a, name=name, session_ring=session_ring, **k)
        self.is_private = is_private
        self.stop_track_clip_buttons.control_count = session_ring.num_tracks

    def set_stop_all_clips_button(self, button):
        self.stop_all_clips_button.set_control_element(button)

    def set_stop_track_clip_buttons(self, buttons):
        self.stop_track_clip_buttons.set_control_element(buttons)
        self._update_stop_track_clip_buttons()

    def __getattr__(self, name):
        if name.startswith('set_selected_scene_launch_button'):
            return self.selected_scene().set_launch_button
        if name.startswith('set_scene_'):
            if name.endswith('_launch_button'):
                return self.scene(int(name.split('_')[(-3)])).set_launch_button
        raise AttributeError

    @stop_all_clips_button.pressed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    @stop_track_clip_buttons.pressed
    def stop_track_clip_buttons(self, button):
        tracks_to_use = self._session_ring.tracks_to_use()
        track_index = self._session_ring.track_offset + button.index
        if track_index < len(tracks_to_use):
            tracks_to_use[track_index].stop_all_clips()

    def _update_stop_clips_led(self, index):
        if index < self.stop_track_clip_buttons.control_count:
            tracks_to_use = self._session_ring.tracks_to_use()
            track_index = self._session_ring.track_offset + index
            button = self.stop_track_clip_buttons[index]
            if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
                button.enabled = True
                track = tracks_to_use[track_index]
                if track.fired_slot_index == -2:
                    button.color = 'Session.StopClipTriggered'
                elif track.playing_slot_index >= 0:
                    button.color = 'Session.StopClip'
                else:
                    button.color = 'Session.StopClipDisabled'
            else:
                button.enabled = False