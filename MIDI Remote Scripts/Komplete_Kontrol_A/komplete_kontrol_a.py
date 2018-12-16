from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ControlSurface, Layer, midi
from ableton.v2.control_surface.components import AutoArmComponent, SessionRecordingComponent, SimpleTrackAssigner
from ableton.v2.base import listens
from ableton.v2.control_surface.mode import ModesComponent, EnablingMode, AddLayerMode
from ableton.v2.control_surface.elements import ButtonMatrixElement
from .transport_component import TransportComponent
from .view_control_component import ViewControlComponent
from .mixer_component import MixerComponent
from .selection_linked_session_ring_component import SelectionLinkedSessionRingComponent
from .clip_launch_component import ClipLaunchComponent
from .background_component import BackgroundComponent
from .detail_clip_component import DetailClipComponent
from .control_element_util import MIDI_CHANNEL, create_button, create_encoder, create_display_line, create_display_matrix, create_sysex_element
from .undo_redo import UndoRedoComponent
from . import sysex
NUM_TRACKS = 8
HELLO_MESSAGE = (midi.CC_STATUS + MIDI_CHANNEL, 1, 0)
GOODBYE_MESSAGE = (midi.CC_STATUS + MIDI_CHANNEL, 2, 0)

class KompleteKontrolA(ControlSurface):

    def __init__(self, *a, **k):
        super(KompleteKontrolA, self).__init__(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_mixer()
            self._create_transport()
            self._create_session_recording()
            self._create_undo_redo()
            self._create_view_control()
            self._create_clip_launch()
            self._create_clip_launch_background()
            self._create_detail_clip()
            self._create_auto_arm()
            self._create_view_based_modes()
            self.__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        self._send_midi(GOODBYE_MESSAGE)
        super(KompleteKontrolA, self).disconnect()

    def port_settings_changed(self):
        self._send_midi(HELLO_MESSAGE)
        super(KompleteKontrolA, self).port_settings_changed()

    def _create_controls(self):
        self._play_button = create_button(16, u'Play_Button')
        self._continue_button = create_button(17, u'Continue_Button')
        self._record_button = create_button(18, u'Record_Button')
        self._count_in_button = create_button(19, u'Count_In_Button')
        self._stop_button = create_button(20, u'Stop_Button')
        self._clear_button = create_button(21, u'Clear_Button')
        self._loop_button = create_button(22, u'Loop_Button')
        self._metronome_button = create_button(23, u'Metronome_Button')
        self._tap_tempo_button = create_button(24, u'Tap_Tempo_Button')
        self._undo_button = create_button(32, u'Undo_Button')
        self._redo_button = create_button(33, u'Redo_Button')
        self._quantize_button = create_button(34, u'Quantize_Button')
        self._automation_button = create_button(35, u'Automation_Button')
        self._mute_button = create_button(67, u'Mute_Button')
        self._solo_button = create_button(68, u'Solo_Button')
        self._clip_launch_button = create_button(96, u'Clip_Launch_Button')
        self._track_stop_button = create_button(97, u'Track_Stop_Button')
        self._vertical_encoder = create_encoder(48, u'Vertical_Encoder')
        self._horizontal_encoder = create_encoder(50, u'Horizontal_Encoder')
        self._jump_encoder = create_encoder(52, u'Jump_Encoder')
        self._loop_encoder = create_encoder(53, u'Loop_Encoder')
        self._encoders_0 = ButtonMatrixElement(rows=[[ create_encoder(index + 80, u'Encoder_{}'.format(index)) for index in xrange(NUM_TRACKS) ]], name=u'Encoders_0')
        self._encoders_1 = ButtonMatrixElement(rows=[[ create_encoder(index + 88, u'Encoder_{}'.format(index)) for index in xrange(NUM_TRACKS) ]], name=u'Encoders_1')
        self._track_name_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_NAME_DISPLAY_HEADER, create_display_line, u'Track_Name_Display', width=11)
        self._track_volume_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_VOLUME_DISPLAY_HEADER, create_display_line, u'Track_Volume_Display', width=12)
        self._track_panning_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_PANNING_DISPLAY_HEADER, create_display_line, u'Track_Panning_Display', width=12)
        self._track_type_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_TYPE_DISPLAY_HEADER, create_sysex_element, u'Track_Type_Display')
        self._track_mute_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_MUTE_DISPLAY_HEADER, create_sysex_element, u'Track_Mute_Display')
        self._track_solo_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_SOLO_DISPLAY_HEADER, create_sysex_element, u'Track_Solo_Display')
        self._track_selection_displays = create_display_matrix(NUM_TRACKS, sysex.TRACK_SELECT_DISPLAY_HEADER, create_sysex_element, u'Track_Selection_Display')

    def _create_mixer(self):
        self._session_ring = SelectionLinkedSessionRingComponent(name=u'Session_Ring', num_tracks=NUM_TRACKS, tracks_to_use=lambda : tuple(self.song.visible_tracks) + tuple(self.song.return_tracks) + (self.song.master_track,), always_snap_track_offset=True)
        self._mixer = MixerComponent(name=u'Mixer', tracks_provider=self._session_ring, track_assigner=SimpleTrackAssigner(), is_enabled=False, layer=Layer(volume_controls=self._encoders_0, pan_controls=self._encoders_1, mute_button=self._mute_button, solo_button=self._solo_button, track_name_displays=self._track_name_displays, track_volume_displays=self._track_volume_displays, track_panning_displays=self._track_panning_displays, track_type_displays=self._track_type_displays, track_mute_displays=self._track_mute_displays, track_solo_displays=self._track_solo_displays, track_selection_displays=self._track_selection_displays))
        self._mixer.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=u'Transport', is_enabled=False, layer=Layer(play_button=self._play_button, continue_button=self._continue_button, stop_button=self._stop_button, loop_button=self._loop_button, metronome_button=self._metronome_button, tap_tempo_button=self._tap_tempo_button, jump_encoder=self._jump_encoder, loop_start_encoder=self._loop_encoder))
        self._transport.set_enabled(True)

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name=u'Session_Recording', is_enabled=False, layer=Layer(automation_button=self._automation_button))
        self._session_recording.set_enabled(True)

    def _create_undo_redo(self):
        self._undo_redo = UndoRedoComponent(name=u'Undo_Redo', is_enabled=False, layer=Layer(undo_button=self._undo_button, redo_button=self._redo_button))
        self._undo_redo.set_enabled(True)

    def _create_view_control(self):
        self._view_control = ViewControlComponent(name=u'View_Control', is_enabled=False, layer=Layer(vertical_encoder=self._vertical_encoder, horizontal_encoder=self._horizontal_encoder))
        self._view_control.set_enabled(True)

    def _create_clip_launch(self):
        self._clip_launch = ClipLaunchComponent(name=u'Clip_Launch', is_enabled=False, layer=Layer(clip_launch_button=self._clip_launch_button, track_stop_button=self._track_stop_button))

    def _create_clip_launch_background(self):
        self._clip_launch_background = BackgroundComponent(name=u'Background', is_enabled=False, layer=Layer(clip_launch_button=self._clip_launch_button, track_stop_button=self._track_stop_button, priority=-1))
        self._clip_launch_background.set_enabled(True)

    def _create_detail_clip(self):
        self._detail_clip = DetailClipComponent(name=u'Detail_Clip', is_enabled=False, layer=Layer(quantize_notes_button=self._quantize_button, delete_notes_button=self._clear_button))
        self._detail_clip.set_enabled(True)

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name=u'Auto_Arm')

    def _create_view_based_modes(self):
        self._view_based_modes = ModesComponent()
        self._view_based_modes.add_mode(u'session', (EnablingMode(self._clip_launch), AddLayerMode(self._transport, Layer(overdub_button=self._record_button, record_button=self._count_in_button))))
        self._view_based_modes.add_mode(u'arrange', AddLayerMode(self._transport, Layer(record_button=self._record_button, overdub_button=self._count_in_button)))
        self.__on_main_view_changed()

    @listens(u'is_view_visible', u'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible(u'Session'):
            self._view_based_modes.selected_mode = u'session'
        else:
            self._view_based_modes.selected_mode = u'arrange'
