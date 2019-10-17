from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import listens, liveobj_valid, mixin
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import BackgroundComponent, SessionRecordingComponent
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ImmediateBehaviour, ModesComponent, ReenterBehaviour
from novation import sysex
from novation.colors import Rgb
from novation.drum_group import DrumGroupComponent
from novation.instrument_control import InstrumentControlMixin
from novation.novation_base import NovationBase
from novation.target_track import ArmedTargetTrackComponent
from novation.track_recording import TrackRecordingComponent
from . import sysex_ids as ids
from .configurable_playable import ConfigurablePlayableComponent
from .elements import Elements
from .session_recording import SessionRecordingMixin
from .skin import skin
DRUM_FEEDBACK_CHANNEL = 1
SCALE_FEEDBACK_CHANNEL = 2

class Launchpad_X(InstrumentControlMixin, NovationBase):
    model_family_code = ids.LP_X_FAMILY_CODE
    element_class = Elements
    session_recording_class = mixin(SessionRecordingMixin, SessionRecordingComponent)
    track_recording_class = mixin(SessionRecordingMixin, TrackRecordingComponent)
    target_track_class = ArmedTargetTrackComponent
    skin = skin

    def on_identified(self, midi_bytes):
        self._elements.firmware_mode_switch.send_value(sysex.DAW_MODE_BYTE)
        self._elements.layout_switch.send_value(sysex.SESSION_LAYOUT_BYTE)
        self._target_track_changed()
        self._drum_group_changed()
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL, SCALE_FEEDBACK_CHANNEL])
        super(Launchpad_X, self).on_identified(midi_bytes)

    def _create_components(self):
        super(Launchpad_X, self)._create_components()
        self._background = BackgroundComponent(name=u'Background', add_nop_listeners=True)
        self._create_recording_modes()
        self._create_mixer_modes()
        self._create_session_modes()
        self._create_note_modes()
        self._create_main_modes()

    def _create_mixer_modes(self):
        self._mixer_modes = ModesComponent(name=u'Mixer_Modes', is_enabled=False, enable_skinning=True, layer=Layer(volume_button=self._elements.scene_launch_buttons_raw[0], pan_button=self._elements.scene_launch_buttons_raw[1], send_a_button=self._elements.scene_launch_buttons_raw[2], send_b_button=self._elements.scene_launch_buttons_raw[3], stop_button=self._elements.scene_launch_buttons_raw[4], mute_button=self._elements.scene_launch_buttons_raw[5], solo_button=self._elements.scene_launch_buttons_raw[6], arm_button=self._elements.scene_launch_buttons_raw[7]))
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 7:8]
        select_none_mode = partial(setattr, self._mixer_modes, u'selected_mode', u'none')
        session_layout_mode = partial(self._elements.layout_switch.send_value, sysex.SESSION_LAYOUT_BYTE)
        self._mixer_modes.add_mode(u'none', session_layout_mode)
        button_fader_layout_mode = partial(self._elements.layout_switch.send_value, sysex.FADERS_LAYOUT_BYTE)

        def add_fader_mode(name, color, is_pan = False):
            control_dict = {u'{}_controls'.format(name): u'button_faders'}
            if is_pan:
                control_dict[u'track_color_controls'] = u'button_fader_color_elements'
            else:
                control_dict[u'static_color_controls'] = u'button_fader_color_elements'
            self._mixer_modes.add_mode(name, (partial(self._elements.button_fader_setup_element.send_value, sysex.HORIZONTAL_ORIENTATION if is_pan else sysex.VERTICAL_ORIENTATION, sysex.BIPOLAR if is_pan else sysex.UNIPOLAR),
             partial(self._mixer.set_static_color_value, color),
             self._clear_send_cache_of_button_fader_color_elements,
             AddLayerMode(self._mixer, Layer(**control_dict)),
             button_fader_layout_mode), behaviour=ReenterBehaviour(on_reenter=select_none_mode))

        add_fader_mode(u'volume', Rgb.GREEN.midi_value)
        add_fader_mode(u'pan', 0, True)
        add_fader_mode(u'send_a', Rgb.VIOLET.midi_value)
        add_fader_mode(u'send_b', Rgb.DARK_BLUE.midi_value)
        self._mixer_modes.add_mode(u'stop', (session_layout_mode, AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(u'mute', (session_layout_mode, AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(u'solo', (session_layout_mode, AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(u'arm', (session_layout_mode, AddLayerMode(self._mixer, Layer(arm_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.selected_mode = u'none'

    def _clear_send_cache_of_button_fader_color_elements(self):
        for element in self._elements.button_fader_color_elements_raw:
            element.clear_send_cache()

    def _create_session_modes(self):
        self._session_modes = ModesComponent(name=u'Session_Modes', is_enabled=False, enable_skinning=True, cycle_modes_with_latching_only=True, layer=Layer(cycle_mode_button=u'session_mode_button', launch_button=u'session_button_color_element'))
        self._session_modes.add_mode(u'launch', AddLayerMode(self._session, Layer(scene_launch_buttons=u'scene_launch_buttons')))
        self._session_modes.add_mode(u'mixer', EnablingMode(self._mixer_modes))
        self._session_modes.selected_mode = u'launch'

    def _create_note_modes(self):
        self._drum_group = DrumGroupComponent(name=u'Drum_Group', is_enabled=False, translation_channel=DRUM_FEEDBACK_CHANNEL, layer=Layer(matrix=u'drum_pads', scroll_up_button=u'left_button', scroll_down_button=u'right_button', scroll_page_up_button=u'up_button', scroll_page_down_button=u'down_button'))
        self._scale_pad_translator = ConfigurablePlayableComponent(SCALE_FEEDBACK_CHANNEL, name=u'Scale_Pads', is_enabled=False, layer=Layer(matrix=u'scale_pads'))
        self._note_modes = ModesComponent(name=u'Note_Modes', is_enabled=False)
        self._note_modes.add_mode(u'scale', (EnablingMode(self._scale_pad_translator), AddLayerMode(self._background, layer=Layer(up_button=u'up_button', down_button=u'down_button', left_button=u'left_button', right_button=u'right_button'))))
        self._note_modes.add_mode(u'drum', EnablingMode(self._drum_group))
        self._note_modes.selected_mode = u'scale'
        self.__on_note_mode_changed.subject = self._note_modes

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name=u'Main_Modes', is_enabled=False, layer=Layer(session_button=u'session_mode_button', note_button=u'note_mode_button', custom_button=u'custom_mode_button'))
        self._main_modes.add_mode(u'session', EnablingMode(self._session_modes), behaviour=ImmediateBehaviour())
        self._main_modes.add_mode(u'note', EnablingMode(self._note_modes), behaviour=ImmediateBehaviour())
        self._main_modes.add_mode(u'custom', None, behaviour=ImmediateBehaviour())
        self._main_modes.selected_mode = u'session'
        self._main_modes.set_enabled(True)
        self.__on_main_mode_changed.subject = self._main_modes

    @listens(u'selected_mode')
    def __on_main_mode_changed(self, mode):
        self._recording_modes.selected_mode = u'track' if mode == u'note' else u'session'
        self._update_controlled_track()

    @listens(u'selected_mode')
    def __on_note_mode_changed(self, mode):
        if self._note_modes.is_enabled():
            self._update_controlled_track()

    def _drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        drum_groud_valid = liveobj_valid(drum_group)
        self._drum_group.set_drum_group_device(drum_group)
        self._elements.note_layout_switch.send_value(sysex.DRUM_LAYOUT_BYTE if drum_groud_valid else sysex.SCALE_LAYOUT_BYTE)
        self._note_modes.selected_mode = u'drum' if drum_groud_valid else u'scale'

    def _is_instrument_mode(self):
        return self._main_modes.selected_mode == u'note'

    def _feedback_velocity_changed(self, feedback_velocity):
        self._elements.scale_feedback_switch.send_value(feedback_velocity)
