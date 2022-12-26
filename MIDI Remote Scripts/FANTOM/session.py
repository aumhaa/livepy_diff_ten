from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens_group, liveobj_valid
import ableton.v3.control_surface.components as SessionComponentBase
from ableton.v3.control_surface.controls import ButtonControl, InputControl
from .control import DisplayControl

class SessionComponent(SessionComponentBase):
    track_select_control = InputControl()
    scene_name_display = DisplayControl()
    stop_all_clips_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)

    def set_stop_all_clips_button(self, button):
        self.stop_all_clips_button.set_control_element(button)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value and value <= self.stop_track_clip_buttons.control_count:
            index = value - 1
            button = self.stop_track_clip_buttons[index].control_element
            if button:
                button.clear_send_cache()
                self._update_stop_clips_led(index)
        else:
            self.stop_all_clips_button.color = 'DefaultButton.Off'

    @stop_all_clips_button.pressed_delayed
    def stop_all_clips_button(self, _):
        self.song.stop_all_clips()

    def _reassign_scenes(self):
        super()._reassign_scenes()
        self._SessionComponent__on_scene_name_changed.replace_subjects((s.scene for s in self._scenes))
        self._update_scene_name_display()

    def _update_scene_name_display(self):
        self.scene_name_display.data = [s.scene for s in self._scenes if liveobj_valid(s.scene)]

    @listens_group('name')
    def __on_scene_name_changed(self, _):
        self._update_scene_name_display()