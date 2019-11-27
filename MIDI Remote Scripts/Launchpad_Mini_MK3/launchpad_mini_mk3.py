from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import BackgroundComponent
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from novation import sysex
from novation.novation_base import NovationBase
from . import sysex_ids as ids
from .elements import Elements

class Launchpad_Mini_MK3(NovationBase):
    model_family_code = ids.LP_MINI_MK3_FAMILY_CODE
    element_class = Elements

    def on_identified(self, midi_bytes):
        self._elements.firmware_mode_switch.send_value(sysex.DAW_MODE_BYTE)
        self._elements.layout_switch.send_value(sysex.SESSION_LAYOUT_BYTE)
        super(Launchpad_Mini_MK3, self).on_identified(midi_bytes)

    def _create_components(self):
        super(Launchpad_Mini_MK3, self)._create_components()
        self._create_stop_solo_mute_modes()
        self._create_background()

    def _create_session_layer(self):
        return super(Launchpad_Mini_MK3, self)._create_session_layer() + Layer(scene_launch_buttons=u'scene_launch_buttons')

    def _create_stop_solo_mute_modes(self):
        self._stop_solo_mute_modes = ModesComponent(name=u'Stop_Solo_Mute_Modes', is_enabled=False, support_momentary_mode_cycling=False, layer=Layer(cycle_mode_button=self._elements.scene_launch_buttons_raw[7]))
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 7:8]
        self._stop_solo_mute_modes.add_mode(u'launch', None, cycle_mode_button_color=u'Mode.Launch.On')
        self._stop_solo_mute_modes.add_mode(u'stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row)), cycle_mode_button_color=u'Session.StopClip')
        self._stop_solo_mute_modes.add_mode(u'solo', AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row)), cycle_mode_button_color=u'Mixer.SoloOn')
        self._stop_solo_mute_modes.add_mode(u'mute', AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row)), cycle_mode_button_color=u'Mixer.MuteOff')
        self._stop_solo_mute_modes.selected_mode = u'launch'
        self._stop_solo_mute_modes.set_enabled(True)

    def _create_background(self):
        self._background = BackgroundComponent(name=u'Background', is_enabled=False, add_nop_listeners=True, layer=Layer(session_mode_button=u'session_mode_button', drums_mode_button=u'drums_mode_button', keys_mode_button=u'keys_mode_button', user_mode_button=u'user_mode_button'))
        self._background.set_enabled(True)
