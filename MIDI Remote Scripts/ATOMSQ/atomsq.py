from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import is_clip_or_slot, is_scene, listens
from ableton.v3.control_surface import ControlSurface, ControlSurfaceSpecification, Layer
from ableton.v3.control_surface.components import MixerComponent, SessionComponent, SessionNavigationComponent, SimpleDeviceNavigationComponent, TranslatingBackgroundComponent, TransportComponent, UndoRedoComponent, ViewControlComponent, ViewToggleComponent
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface.mode import AddLayerMode, ModesComponent
from . import midi
from .button_labels import ButtonLabelsComponent
from .channel_strip import ChannelStripComponent
from .colors import LIVE_COLOR_INDEX_TO_RGB
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .launch_and_stop import LaunchAndStopComponent
from .simple_device import SimpleDeviceParameterComponent
from .skin import skin

class Specification(ControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = skin
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    link_session_ring_to_track_selection = True
    identity_response_id_bytes = midi.PRODUCT_ID_BYTES
    hello_messages = (midi.NATIVE_MODE_ON_MESSAGE,)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    color_for_liveobj_function = --- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              is_clip_or_slot
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_GLOBAL              is_scene
               10  LOAD_FAST                'obj'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  POP_JUMP_IF_FALSE    30  'to 30'
             16_0  COME_FROM             6  '6'
               16  LOAD_GLOBAL              LIVE_COLOR_INDEX_TO_RGB
               18  LOAD_METHOD              get
               20  LOAD_FAST                'obj'
               22  LOAD_ATTR                color_index
               24  LOAD_CONST               0
               26  CALL_METHOD_2         2  '2 positional arguments'
               28  RETURN_VALUE_LAMBDA
             30_0  COME_FROM            14  '14'

 L.  45        30  LOAD_CONST               None
               32  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1


class ATOMSQ(ControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def setup(self):
        self._create_transport()
        self._create_undo()
        self._create_view_toggle()
        self._create_device_parameters()
        self._create_translating_background()
        self._create_device_navigation()
        self._create_launch_and_stop()
        self._create_session()
        self._create_mixer()
        self._create_view_control()
        self._create_button_labels()
        self._create_lower_pad_modes()
        self._create_main_modes()

    def on_identified(self, response_bytes):
        if self._main_modes.selected_mode == 'instrument':
            self.schedule_message(1, self.elements.upper_firmware_toggle_switch.send_value, 1)
        if self._main_modes.selected_mode != 'song':
            self.schedule_message(1, self.elements.lower_firmware_toggle_switch.send_value, 1)
        super().on_identified(response_bytes)

    def _create_transport(self):
        self._transport = TransportComponent(is_enabled=False,
          layer=Layer(arrangement_position_encoder='display_encoder',
          tempo_coarse_encoder='display_encoder_with_shift',
          play_button='play_button',
          loop_button='play_button_with_shift',
          stop_button='stop_button',
          view_based_record_button='record_button',
          metronome_button='click_button',
          capture_midi_button='record_button_with_shift',
          prev_cue_button='display_left_button',
          next_cue_button='display_right_button'))
        self._transport.add_control('sq_shift_button', ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On'))
        self._transport.sq_shift_button.set_control_element(self.elements.shift_button)
        self._transport.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(is_enabled=False,
          layer=Layer(undo_button='stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(is_enabled=False,
          layer=Layer(main_view_toggle_button='bank_a_button',
          browser_view_toggle_button='bank_b_button',
          detail_view_toggle_button='bank_d_button',
          clip_view_toggle_button='bank_h_button'))

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(is_enabled=False,
          quantized_parameter_sensitivity=0.3,
          layer=Layer(device_name_display='device_name_display'))
        self._device_parameters.set_enabled(True)

    def _create_translating_background(self):
        self._translating_background = TranslatingBackgroundComponent(is_enabled=False,
          translation_channel=(midi.USER_MODE_START_CHANNEL),
          layer=Layer(encoders='encoders', channel_selection_buttons='display_buttons'))

    def _create_device_navigation(self):
        self._device_navigation = SimpleDeviceNavigationComponent(is_enabled=False,
          layer=Layer(prev_button='display_buttons_raw[1]',
          next_button='display_buttons_raw[2]'))

    def _create_launch_and_stop(self):
        self._launch_and_stop = LaunchAndStopComponent(name='Launch_And_Stop',
          is_enabled=False,
          layer=Layer(clip_launch_button='display_buttons_raw[3]',
          scene_launch_button='display_buttons_raw[4]',
          track_stop_button='display_buttons_raw[5]'))

    def _create_session(self):
        self._session = SessionComponent(is_enabled=False,
          layer=Layer(clip_launch_buttons='upper_pads',
          scene_0_launch_button='plus_button'))
        self._session_navigation = SessionNavigationComponent(is_enabled=False,
          layer=Layer(up_button='up_button_with_shift',
          down_button='down_button_with_shift'))
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(is_enabled=False,
          channel_strip_component_type=ChannelStripComponent,
          layer=Layer(target_track_track_name_display='track_name_display'))
        self._mixer.set_enabled(True)

    def _create_view_control(self):
        self._view_control = ViewControlComponent(is_enabled=False,
          layer=Layer(next_track_button='right_button',
          prev_track_button='left_button',
          next_scene_button='down_button',
          prev_scene_button='up_button'))
        self._view_control.set_enabled(True)

    def _create_button_labels(self):
        self._button_labels = ButtonLabelsComponent(is_enabled=False,
          layer=Layer(display_lines='button_label_displays'))
        self._button_labels.set_enabled(True)

    def _create_lower_pad_modes(self):
        self._lower_pad_modes = ModesComponent(name='Lower_Pad_Modes',
          is_enabled=False,
          layer=Layer(cycle_mode_button='minus_button'))
        self._lower_pad_modes.add_mode('select',
          (AddLayerMode(self._mixer, Layer(track_select_buttons='lower_pads'))),
          cycle_mode_button_color='Session.StopClipDisabled')
        self._lower_pad_modes.add_mode('stop',
          (AddLayerMode(self._session, Layer(stop_track_clip_buttons='lower_pads'))),
          cycle_mode_button_color='Session.StopClip')
        self._lower_pad_modes.selected_mode = 'select'

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name='Main_Modes',
          is_enabled=False,
          layer=Layer(song_button='song_mode_button',
          instrument_button='instrument_mode_button',
          editor_button='editor_mode_button',
          user_button='user_mode_button'))
        device_params_mode = AddLayerMode(self._device_parameters, Layer(parameter_controls='encoders'))
        enable_lower_fw_functions = partial(self.elements.lower_firmware_toggle_switch.send_value, 1)
        disable_upper_fw_functions = partial(self.elements.upper_firmware_toggle_switch.send_value, 0)
        self._main_modes.add_mode('song', (
         partial(self.elements.lower_firmware_toggle_switch.send_value, 0),
         disable_upper_fw_functions,
         self._view_toggle,
         self._launch_and_stop,
         self._session,
         self._lower_pad_modes,
         AddLayerMode(self._mixer, Layer(target_track_volume_control='encoders_raw[0]',
           target_track_pan_control='encoders_raw[1]',
           target_track_send_controls='encoders_2_thru_7',
           target_track_solo_button='display_buttons_raw[0]',
           target_track_mute_button='display_buttons_raw[1]',
           target_track_arm_button='display_buttons_raw[2]',
           crossfader_control='touch_strip'))))
        self._main_modes.add_mode('instrument', (
         enable_lower_fw_functions,
         partial(self.elements.upper_firmware_toggle_switch.send_value, 1),
         device_params_mode))
        self._main_modes.add_mode('editor', (
         enable_lower_fw_functions,
         disable_upper_fw_functions,
         device_params_mode,
         self._device_navigation,
         AddLayerMode(self._device_parameters, Layer(device_lock_button='display_buttons_raw[0]',
           device_on_off_button='display_buttons_raw[3]',
           prev_bank_button='display_buttons_raw[4]',
           next_bank_button='display_buttons_raw[5]'))))
        self._main_modes.add_mode('user', (
         enable_lower_fw_functions,
         disable_upper_fw_functions,
         self._translating_background))
        self._main_modes.selected_mode = 'instrument'
        self._main_modes.set_enabled(True)
        self._ATOMSQ__on_main_modes_changed.subject = self._main_modes

    @listens('selected_mode')
    def __on_main_modes_changed(self, mode):
        self._button_labels.show_button_labels_for_mode(mode)
        self.elements.track_name_display.clear_send_cache()
        self.elements.device_name_display.clear_send_cache()