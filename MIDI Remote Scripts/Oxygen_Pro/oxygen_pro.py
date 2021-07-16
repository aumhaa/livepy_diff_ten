from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import ControlSurface, Layer
from ableton.v2.control_surface.components import MixerComponent, SessionNavigationComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, TransportComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ModesComponent
from novation.simple_device import SimpleDeviceParameterComponent
from .elements import Elements, SESSION_HEIGHT, SESSION_WIDTH
from .session import SessionComponent

class Oxygen_Pro(ControlSurface):

    def __init__(self, *a, **k):
        (super(Oxygen_Pro, self).__init__)(*a, **k)
        with self.component_guard():
            self._elements = Elements()
            with inject(element_container=(const(self._elements))).everywhere():
                self._create_transport()
                self._create_undo_redo()
                self._create_device_parameters()
                self._create_session()
                self._create_mixer()
                self._create_record_modes()
        self._Oxygen_Pro__on_main_view_changed.subject = self.application.view

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(loop_button='loop_button',
          stop_button='stop_button',
          play_button='play_button'))
        self._transport.set_enabled(True)

    def _create_undo_redo(self):
        self._undo_redo = UndoRedoComponent(name='Undo_Redo',
          is_enabled=False,
          layer=Layer(undo_button='back_button'))
        self._undo_redo.set_enabled(True)

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name='Device_Parameters',
          is_enabled=False,
          layer=Layer(parameter_controls='knobs'))
        self._device_parameters.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(name='Session_Ring',
          num_tracks=SESSION_WIDTH,
          num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name='Session',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(clip_launch_buttons='pads',
          scene_launch_buttons='scene_launch_buttons',
          scene_encoder='encoder'))
        self._session.selected_scene().set_launch_button(self._elements.encoder_push_button)
        self._session.set_enabled(True)
        self._session_navigation = SessionNavigationComponent(name='Session_Navigation',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(left_button='bank_left_button', right_button='bank_right_button'))
        self._session_navigation.set_up_button(self._elements.rewind_button)
        self._session_navigation.set_down_button(self._elements.fastforward_button)
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          is_enabled=False,
          auto_name=True,
          tracks_provider=(self._session_ring),
          track_assigner=(SimpleTrackAssigner()),
          layer=Layer(volume_controls='faders', arm_buttons='fader_buttons'))
        self._mixer.master_strip().set_volume_control(self._elements.master_fader)
        self._mixer.set_enabled(True)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name='Session_Record',
          is_enabled=False,
          layer=Layer(record_button='record_button'))
        self._record_modes = ModesComponent(name='Record_Modes')
        self._record_modes.add_mode('session', EnablingMode(self._session_record))
        self._record_modes.add_mode('arrange', AddLayerMode((self._transport), layer=Layer(record_button='record_button')))
        self._Oxygen_Pro__on_main_view_changed()

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible('Session'):
            self._record_modes.selected_mode = 'session'
        else:
            self._record_modes.selected_mode = 'arrange'