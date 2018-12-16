from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class DisplayingMixerComponent(MixerComponent):
    u""" Special mixer class that displays the Mute/Solo state of the selected track """

    def __init__(self, num_tracks):
        MixerComponent.__init__(self, num_tracks)
        self._selected_tracks = []
        self._display = None
        self._mute_button = None
        self._solo_button = None
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._selected_tracks = None
        MixerComponent.disconnect(self)
        self._display = None

    def set_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._display = display

    def set_solo_button(self, button):
        assert button == None or isinstance(button, ButtonElement) and button.is_momentary()
        self.selected_strip().set_solo_button(button)
        if self._solo_button != button:
            if self._solo_button != None:
                self._solo_button.remove_value_listener(self._solo_value)
            self._solo_button = button
            if self._solo_button != None:
                self._solo_button.add_value_listener(self._solo_value)
            self.update()

    def set_mute_button(self, button):
        assert button == None or isinstance(button, ButtonElement) and button.is_momentary()
        self.selected_strip().set_mute_button(button)
        if self._mute_button != button:
            if self._mute_button != None:
                self._mute_button.remove_value_listener(self._mute_value)
            self._mute_button = button
            if self._mute_button != None:
                self._mute_button.add_value_listener(self._mute_value)
            self.update()

    def _on_timer(self):
        sel_track = None
        while len(self._selected_tracks) > 0:
            track = self._selected_tracks[-1]
            if track != None and track.has_midi_input and track.can_be_armed and not track.arm:
                sel_track = track
                break
            del self._selected_tracks[-1]

        if sel_track != None:
            found_recording_clip = False
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            for track in tracks:
                if track.can_be_armed and track.arm:
                    if check_arrangement:
                        found_recording_clip = True
                        break
                    else:
                        playing_slot_index = track.playing_slot_index
                        if playing_slot_index in range(len(track.clip_slots)):
                            slot = track.clip_slots[playing_slot_index]
                            if slot.has_clip and slot.clip.is_recording:
                                found_recording_clip = True
                                break

            if not found_recording_clip:
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed and track.arm and track != sel_track:
                            track.arm = False

                sel_track.arm = True
                sel_track.view.select_instrument()
        self._selected_tracks = []

    def _solo_value(self, value):
        assert self._solo_button != None
        assert value in range(128)
        if self._display != None and self.song().view.selected_track not in (self.song().master_track, None):
            if value != 0:
                track = self.song().view.selected_track
                display_string = str(track.name) + u': Solo '
                if track.solo:
                    display_string += u'On'
                else:
                    display_string += u'Off'
                self._display.display_message(display_string)
            else:
                self._display.update()

    def _mute_value(self, value):
        assert self._mute_button != None
        assert value in range(128)
        if self._display != None and self.song().view.selected_track not in (self.song().master_track, None):
            if value != 0:
                track = self.song().view.selected_track
                display_string = str(track.name) + u': Mute '
                if track.mute:
                    display_string += u'On'
                else:
                    display_string += u'Off'
                self._display.display_message(display_string)
            else:
                self._display.update()

    def _next_track_value(self, value):
        MixerComponent._next_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)

    def _prev_track_value(self, value):
        MixerComponent._prev_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)
