from __future__ import absolute_import, print_function, unicode_literals
from itertools import ifilter
from ...base import listens, listens_group
from ...control_surface import Component

class AutoArmComponent(Component):
    u"""
    Component that implictly arms tracks to keep the selected track
    always armed while there is no compatible red-armed track.
    """

    def __init__(self, *a, **k):
        super(AutoArmComponent, self).__init__(*a, **k)
        self._on_tracks_changed.subject = self.song
        self._on_exclusive_arm_changed.subject = self.song
        self._on_tracks_changed()
        self._on_selected_track_changed.subject = self.song.view

    @property
    def needs_restore_auto_arm(self):
        song = self.song
        exclusive_arm = song.exclusive_arm
        return self.is_enabled() and self.can_auto_arm_track(song.view.selected_track) and not song.view.selected_track.arm and any(ifilter(lambda track: (exclusive_arm or self.can_auto_arm_track(track)) and track.can_be_armed and track.arm, song.tracks))

    def track_can_be_armed(self, track):
        return track.can_be_armed and track.has_midi_input

    def can_auto_arm(self):
        return self.is_enabled() and not self.needs_restore_auto_arm

    def can_auto_arm_track(self, track):
        return self.track_can_be_armed(track)

    @listens(u'selected_track')
    def _on_selected_track_changed(self):
        self.update()

    def update(self):
        super(AutoArmComponent, self).update()
        song = self.song
        selected_track = song.view.selected_track
        for track in song.tracks:
            if self.track_can_be_armed(track):
                track.implicit_arm = self.can_auto_arm() and selected_track == track and self.can_auto_arm_track(track)

    @listens(u'tracks')
    def _on_tracks_changed(self):
        tracks = filter(lambda t: t.can_be_armed, self.song.tracks)
        self._on_arm_changed.replace_subjects(tracks)
        self._on_input_routing_type_changed.replace_subjects(tracks)
        self._on_frozen_state_changed.replace_subjects(tracks)

    @listens(u'exclusive_arm')
    def _on_exclusive_arm_changed(self):
        self.update()

    @listens_group(u'arm')
    def _on_arm_changed(self, track):
        self.update()

    @listens_group(u'input_routing_type')
    def _on_input_routing_type_changed(self, track):
        self.update()

    @listens_group(u'is_frozen')
    def _on_frozen_state_changed(self, track):
        self.update()
