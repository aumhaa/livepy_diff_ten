from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.components import track_is_recording, track_playing_slot

class TrackRecordingComponent(SessionRecordingComponentBase):

    def __init__(self, target_track_component, *a, **k):
        super(TrackRecordingComponent, self).__init__(*a, **k)
        self._target_track_component = target_track_component

    def _trigger_recording(self):
        track = self._target_track_component.target_track
        if self._track_can_record(track):
            self._record_to_track(track)
        else:
            super(TrackRecordingComponent, self)._trigger_recording()

    def _record_to_track(self, track):
        playing_slot = track_playing_slot(track)
        if not track_is_recording(track) and playing_slot is not None:
            self.song.overdub = not self.song.overdub
            if not self.song.is_playing:
                self.song.is_playing = True
        elif not self._stop_recording():
            self._prepare_new_slot(track)
            self._start_recording()

    def _prepare_new_slot(self, track):
        try:
            slot_index = list(self.song.scenes).index(self.song.view.selected_scene)
            track.stop_all_clips(False)
            self._jump_to_next_slot(track, slot_index)
        except Live.Base.LimitationError:
            self._handle_limitation_error_on_scene_creation()

    def _track_can_record(self, track):
        return track in self.song.tracks and track.can_be_armed
