u"""
Component that automatically selects the playing clip in the selected track.
"""
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import index_if, nop, listens, task
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import AddLayerMode
from .consts import MessageBoxText
from .messenger_mode_component import MessengerModesComponent

class SelectPlayingClipComponent(MessengerModesComponent):
    action_button = ButtonControl(color=u'DefaultButton.Alert')

    def __init__(self, playing_clip_above_layer = None, playing_clip_below_layer = None, *a, **k):
        super(SelectPlayingClipComponent, self).__init__(*a, **k)
        self._update_mode_task = self._tasks.add(task.sequence(task.delay(1), task.run(self._update_mode)))
        self._update_mode_task.kill()
        self.add_mode(u'default', None)
        self.add_mode(u'above', [AddLayerMode(self, playing_clip_above_layer)], message=MessageBoxText.PLAYING_CLIP_ABOVE_SELECTED_CLIP)
        self.add_mode(u'below', [AddLayerMode(self, playing_clip_below_layer)], message=MessageBoxText.PLAYING_CLIP_BELOW_SELECTED_CLIP)
        self.selected_mode = u'default'
        self.notify_when_enabled = True
        self._on_detail_clip_changed.subject = self.song.view
        self._on_playing_slot_index_changed.subject = self.song.view.selected_track
        self._notification_reference = partial(nop, None)

    @action_button.pressed
    def action_button(self, button):
        self._go_to_playing_clip()

    @listens(u'detail_clip')
    def _on_detail_clip_changed(self):
        self._update_mode_task.restart()

    @listens(u'playing_slot_index')
    def _on_playing_slot_index_changed(self):
        self._update_mode_task.restart()

    def _go_to_playing_clip(self):
        song_view = self.song.view
        playing_clip_slot = self._playing_clip_slot()
        if playing_clip_slot:
            song_view.highlighted_clip_slot = playing_clip_slot
            song_view.detail_clip = playing_clip_slot.clip
            self._hide_notification()

    def _hide_notification(self):
        if self._notification_reference() is not None:
            self._notification_reference().hide()

    def show_notification(self, display_text):
        self._notification_reference = super(SelectPlayingClipComponent, self).show_notification(display_text, blink_text=MessageBoxText.SELECTED_CLIP_BLINK, notification_time=-1)

    def _selected_track_clip_is_playing(self):
        playing_clip_slot = self._playing_clip_slot()
        return not (playing_clip_slot and playing_clip_slot.clip != self.song.view.detail_clip)

    def _playing_clip_slot(self):
        track = self.song.view.selected_track
        try:
            playing_slot_index = track.playing_slot_index
            slot = track.clip_slots[playing_slot_index] if 0 <= playing_slot_index < len(track.clip_slots) else None
            return slot
        except RuntimeError:
            pass

    def _selected_track_clip_is_above_playing_clip(self):
        song_view = self.song.view
        track = song_view.selected_track
        playing_slot_index = track.playing_slot_index
        selected_index = index_if(lambda slot: slot == song_view.highlighted_clip_slot, track.clip_slots)
        return playing_slot_index <= selected_index

    def _update_mode(self):
        if not self._selected_track_clip_is_playing():
            if self._selected_track_clip_is_above_playing_clip():
                self.selected_mode = u'above'
            else:
                self.selected_mode = u'below'
        else:
            self.selected_mode = u'default'
            self._hide_notification()
