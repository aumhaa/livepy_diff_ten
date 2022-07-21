from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens, liveobj_valid
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, Layer
from ableton.v3.control_surface.components import ArmedTargetTrackComponent, MixerComponent, ModifierBackgroundComponent, SessionComponent, SessionNavigationComponent, SessionOverviewComponent, TranslatingBackgroundComponent, TransportComponent, UndoRedoComponent, ViewToggleComponent
from ableton.v3.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from . import midi
from .colors import LIVE_COLOR_INDEX_TO_RGB
from .drum_group import DrumGroupComponent
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .keyboard import KeyboardComponent
from .skin import skin

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = skin
    target_track_component_type = ArmedTargetTrackComponent
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    identity_request = midi.NATIVE_MODE_ON_MESSAGE
    custom_identity_response = (191, 127, 127)


class ATOM(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def _create_control_surface(self):
        self._mixer = MixerComponent()
        self._create_modifier_background()
        self._create_transport()
        self._create_undo()
        self._create_view_toggle()
        self._create_session()
        self._create_encoder_modes()
        self._create_session_navigation_modes()
        self._create_keyboard()
        self._create_drum_group()
        self._create_note_modes()
        self._create_pad_modes()
        self._create_user_assignments_mode()
        self._ATOM__on_pad_mode_changed.subject = self._pad_modes

    def disconnect(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super().disconnect()

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super().port_settings_changed()

    def _create_modifier_background(self):
        self._modifier_background = ModifierBackgroundComponent(is_enabled=False,
          layer=Layer(shift='shift_button', zoom='zoom_button'))
        self._modifier_background.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(is_enabled=False,
          layer=Layer(play_button='play_button',
          loop_button='play_button_with_shift',
          stop_button='stop_button',
          metronome_button='click_button',
          view_based_record_button='record_button'))
        self._transport.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(is_enabled=False,
          layer=Layer(undo_button='stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(is_enabled=False,
          layer=Layer(detail_view_toggle_button='show_hide_button',
          main_view_toggle_button='preset_button'))
        self._view_toggle.set_enabled(True)

    def _create_session(self):
        self._session = SessionComponent(color_for_obj_function=(lambda obj: LIVE_COLOR_INDEX_TO_RGB.get(obj.color_index, 0)))
        self._session_navigation = SessionNavigationComponent(is_enabled=False,
          layer=Layer(left_button='left_button', right_button='right_button'))
        self._session_navigation.set_enabled(True)
        self._session_overview = SessionOverviewComponent(is_enabled=False,
          layer=Layer(button_matrix='pads_with_zoom'))

    def _create_encoder_modes(self):
        self._encoder_modes = ModesComponent(name='Encoder_Modes', enable_skinning=True)
        self._encoder_modes.add_mode('volume', AddLayerMode(self._mixer, Layer(volume_controls='encoders')))
        self._encoder_modes.add_mode('pan', AddLayerMode(self._mixer, Layer(pan_controls='encoders')))
        self._encoder_modes.add_mode('send_a', AddLayerMode(self._mixer, Layer(send_a_controls='encoders')))
        self._encoder_modes.add_mode('send_b', AddLayerMode(self._mixer, Layer(send_b_controls='encoders')))
        self._encoder_modes.selected_mode = 'volume'

    def _create_session_navigation_modes(self):
        self._session_navigation_modes = ModesComponent(name='Session_Navigation_Modes',
          is_enabled=False,
          enable_skinning=True,
          layer=Layer(cycle_mode_button='bank_button'))
        self._session_navigation_modes.add_mode('default', AddLayerMode((self._session_navigation),
          layer=Layer(up_button='up_button', down_button='down_button')))
        self._session_navigation_modes.add_mode('paged', AddLayerMode((self._session_navigation),
          layer=Layer(page_up_button='up_button',
          page_down_button='down_button',
          page_left_button='left_button',
          page_right_button='right_button')))
        self._session_navigation_modes.selected_mode = 'default'

    def _create_keyboard(self):
        self._keyboard = KeyboardComponent((midi.KEYBOARD_CHANNEL),
          name='Keyboard',
          is_enabled=False,
          layer=Layer(matrix='pads',
          scroll_up_button='up_button',
          scroll_down_button='down_button'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(is_enabled=False,
          translation_channel=(midi.DRUM_CHANNEL),
          layer=Layer(matrix='pads',
          scroll_page_up_button='up_button',
          scroll_page_down_button='down_button'))

    def _create_note_modes(self):
        self._note_modes = ModesComponent(name='Note_Modes', is_enabled=False)
        self._note_modes.add_mode('keyboard', self._keyboard)
        self._note_modes.add_mode('drum', self._drum_group)
        self._note_modes.selected_mode = 'keyboard'

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes',
          is_enabled=False,
          layer=Layer(session_button='full_level_button',
          note_button='note_repeat_button',
          channel_button='select_button',
          encoder_modes_button='setup_button'))
        self._pad_modes.add_mode('session', (
         AddLayerMode(self._background, Layer(unused_pads='pads_with_shift')),
         AddLayerMode(self._session, Layer(clip_launch_buttons='pads',
           scene_launch_buttons='pads_column_3_with_shift')),
         self._session_overview,
         self._session_navigation_modes))
        self._pad_modes.add_mode('note', self._note_modes)
        self._pad_modes.add_mode('channel', (
         self._elements.pads.reset,
         AddLayerMode(self._mixer, Layer(arm_buttons='pads_row_0',
           solo_buttons='pads_row_1',
           track_select_buttons='pads_row_2')),
         AddLayerMode(self._session, Layer(stop_track_clip_buttons='pads_row_3')),
         self._session_navigation_modes))
        self._pad_modes.add_mode('encoder_modes',
          (LayerMode(self._encoder_modes, Layer(volume_button='pads_raw[0]',
          pan_button='pads_raw[1]',
          send_a_button='pads_raw[2]',
          send_b_button='pads_raw[3]'))),
          behaviour=(MomentaryBehaviour()))
        self._pad_modes.selected_mode = 'session'
        self._pad_modes.set_enabled(True)

    def _create_user_assignments_mode(self):
        self._translating_background = TranslatingBackgroundComponent(is_enabled=False,
          translation_channel=(midi.USER_CHANNEL),
          layer=Layer(note_repeat_button='note_repeat_button',
          full_level_button='full_level_button',
          bank_button='bank_button',
          preset_button='preset_button',
          show_hide_button='show_hide_button',
          nudge_button='nudge_button',
          set_loop_button='set_loop_button',
          setup_button='setup_button',
          up_button='up_button',
          down_button='down_button',
          left_button='left_button',
          right_button='right_button',
          select_button='select_button',
          click_button='click_button',
          record_button='record_button',
          play_button='play_button',
          stop_button='stop_button',
          pads='pads',
          encoders='encoders'))
        self._top_level_modes = ModesComponent(name='Top_Level_Modes',
          is_enabled=False,
          enable_skinning=True,
          support_momentary_mode_cycling=False,
          layer=Layer(cycle_mode_button='editor_button'))
        self._top_level_modes.add_mode('default', self.refresh_state)
        self._top_level_modes.add_mode('user', self._translating_background)
        self._top_level_modes.selected_mode = 'default'
        self._top_level_modes.set_enabled(True)

    def drum_group_changed(self, drum_group):
        self._drum_group.set_drum_group_device(drum_group)
        self._note_modes.selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'

    @listens('selected_mode')
    def __on_pad_mode_changed(self, selected_mode):
        self.set_is_observing_instruments(selected_mode == 'note')