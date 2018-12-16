from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.component import Component
from ableton.v2.control_surface.control import ButtonControl

class ClipLaunchComponent(Component):
    clip_launch_button = ButtonControl()
    track_stop_button = ButtonControl()

    @clip_launch_button.pressed
    def clip_launch_button(self, _):
        track = self.song.view.selected_track
        if track == self.song.master_track:
            self.song.view.selected_scene.fire()
        else:
            slot = self.song.view.highlighted_clip_slot
            if slot:
                slot.fire()

    @track_stop_button.pressed
    def track_stop_button(self, _):
        track = self.song.view.selected_track
        if track == self.song.master_track:
            self.song.stop_all_clips()
        elif track in self.song.tracks:
            track.stop_all_clips()
