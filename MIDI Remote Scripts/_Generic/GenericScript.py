from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
from functools import partial
import _Framework.ButtonElement as ButtonElement
import _Framework.ButtonMatrixElement as ButtonMatrixElement
import _Framework.ControlSurface as ControlSurface
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.Layer as Layer
import _Framework.TransportComponent as TransportComponent
from .SpecialMixerComponent import SpecialMixerComponent

def is_valid_midi_channel(integer):
    return 0 <= integer < 16


def is_valid_midi_identifier(integer):
    return 0 <= integer < 128


def has_specification_for(control, specifications):
    return is_valid_midi_identifier(specifications.get(control, -1))


class GenericScript(ControlSurface):

    def __init__(self, c_instance, macro_map_mode, volume_map_mode, device_controls, transport_controls, volume_controls, trackarm_controls, bank_controls, descriptions=None, mixer_options=None):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            global_channel = 0
            if descriptions:
                if list(descriptions.keys()).count('INPUTPORT') > 0:
                    self._suggested_input_port = descriptions['INPUTPORT']
                if list(descriptions.keys()).count('OUTPUTPORT') > 0:
                    self._suggested_output_port = descriptions['OUTPUTPORT']
                if list(descriptions.keys()).count('CHANNEL') > 0:
                    global_channel = descriptions['CHANNEL']
                    if not is_valid_midi_channel(global_channel):
                        global_channel = 0
                    if list(descriptions.keys()).count('PAD_TRANSLATION') > 0:
                        self.set_pad_translations(descriptions['PAD_TRANSLATION'])
            self._init_mixer_component(volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode)
            self._init_device_component(device_controls, bank_controls, global_channel, macro_map_mode)
            self._init_transport_component(transport_controls, global_channel)

    def handle_sysex(self, midi_bytes):
        pass

    def _init_mixer_component(self, volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode):
        momentary_buttons = mixer_options is not None and 'NOTOGGLE' in list(mixer_options.keys())
        MixerButton = partial(ButtonElement, momentary_buttons, MIDI_CC_TYPE, global_channel)

        def make_mixer_encoder(cc, channel, name):
            if is_valid_midi_identifier(cc):
                if is_valid_midi_channel(channel):
                    return EncoderElement(MIDI_CC_TYPE, channel, cc, volume_map_mode, name=name)

        def make_mixer_button(control, name):
            return MixerButton((mixer_options[control]), name=name)

        if volume_controls != None:
            if trackarm_controls != None:
                num_strips = max(len(volume_controls), len(trackarm_controls))
                send_info = []
                mixer = SpecialMixerComponent(num_strips, name='Mixer')
                mixer.master_strip().name = 'Master_Channel_Strip'
                mixer.selected_strip().name = 'Selected_Channel_Strip'
                if mixer_options != None:
                    if has_specification_for('MASTERVOLUME', mixer_options):
                        if is_valid_midi_identifier(mixer_options['MASTERVOLUME']):
                            mixer.master_strip().layer = Layer(volume_control=(make_mixer_encoder(mixer_options['MASTERVOLUME'], global_channel, 'Master_Volume_Control')))
                    for send in range(mixer_options.get('NUMSENDS', 0)):
                        send_info.append(mixer_options[('SEND%d' % (send + 1))])

                    layer_specs = {}
                    if has_specification_for('NEXTBANK', mixer_options):
                        layer_specs['bank_up_button'] = make_mixer_button('NEXTBANK', 'Mixer_Next_Bank_Button')
                    if has_specification_for('PREVBANK', mixer_options):
                        layer_specs['bank_down_button'] = make_mixer_button('PREVBANK', 'Mixer_Previous_Bank_Button')
                    mixer.layer = Layer(**layer_specs)
                for track in range(num_strips):
                    strip = mixer.channel_strip(track)
                    strip.name = 'Channel_Strip_' + str(track)
                    layer_specs = {}
                    if 0 <= track < len(volume_controls):
                        channel = global_channel
                        cc = volume_controls[track]
                        if isinstance(volume_controls[track], (tuple, list)):
                            cc = volume_controls[track][0]
                            if is_valid_midi_channel(volume_controls[track][1]):
                                channel = volume_controls[track][1]
                        if is_valid_midi_identifier(cc):
                            if is_valid_midi_channel(channel):
                                layer_specs['volume_control'] = make_mixer_encoder(cc, channel, str(track) + '_Volume_Control')
                    if 0 <= track < len(trackarm_controls):
                        if is_valid_midi_identifier(trackarm_controls[track]):
                            layer_specs['arm_button'] = MixerButton((trackarm_controls[track]),
                              name=(str(track) + '_Arm_Button'))
                    send_controls_raw = []
                    for index, send in enumerate(send_info):
                        if 0 <= track < len(send):
                            channel = global_channel
                            cc = send[track]
                            if isinstance(send[track], (tuple, list)):
                                cc = send[track][0]
                                if is_valid_midi_channel(send[track][1]):
                                    channel = send[track][1]
                            if is_valid_midi_identifier(cc):
                                if is_valid_midi_channel(channel):
                                    send_controls_raw.append(make_mixer_encoder(cc,
                                      channel,
                                      name=('%d_Send_%d_Control' % (track, index))))

                    if len(send_controls_raw) > 0:
                        layer_specs['send_controls'] = ButtonMatrixElement(rows=[
                         send_controls_raw])
                    else:
                        strip.layer = Layer(**layer_specs)

    def _init_device_component(self, device_controls, bank_controls, global_channel, macro_map_mode):
        is_momentary = True
        DeviceButton = partial(ButtonElement, is_momentary, MIDI_CC_TYPE)

        def make_bank_button(control, name, is_momentary=True):
            return DeviceButton(global_channel, (bank_controls[control]), name=name)

        if device_controls:
            device = DeviceComponent(device_selection_follows_track_selection=True,
              name='Device_Component')
            layer_specs = {}
            if bank_controls:
                if has_specification_for('NEXTBANK', bank_controls):
                    layer_specs['bank_next_button'] = make_bank_button('NEXTBANK', 'Device_Next_Bank_Button')
                if has_specification_for('PREVBANK', bank_controls):
                    layer_specs['bank_prev_button'] = make_bank_button('PREVBANK', 'Device_Previous_Bank_Button')
                if has_specification_for('TOGGLELOCK', bank_controls):
                    layer_specs['lock_button'] = make_bank_button('TOGGLELOCK', 'Device_Lock_Button')
                bank_buttons_raw = []
                for index in range(8):
                    key = 'BANK' + str(index + 1)
                    if key in list(bank_controls.keys()):
                        control_info = bank_controls[key]
                        channel = global_channel
                        cc = control_info
                        if isinstance(control_info, (tuple, list)):
                            cc = control_info[0]
                            if is_valid_midi_channel(control_info[1]):
                                channel = control_info[1]
                        if is_valid_midi_identifier(cc):
                            if is_valid_midi_channel(channel):
                                name = 'Device_Bank_' + str(index) + '_Button'
                                bank_buttons_raw.append(DeviceButton(channel, cc, name=name))

                if len(bank_buttons_raw) > 0:
                    layer_specs['bank_buttons'] = ButtonMatrixElement(rows=[
                     bank_buttons_raw])
            parameter_encoders_raw = []
            for index, control_info in enumerate(device_controls):
                channel = global_channel
                cc = control_info
                if isinstance(control_info, (tuple, list)):
                    cc = control_info[0]
                    if is_valid_midi_channel(control_info[1]):
                        channel = control_info[1]
                if is_valid_midi_identifier(cc):
                    if is_valid_midi_channel(channel):
                        name = 'Device_Parameter_%d_Control' % index
                        parameter_encoders_raw.append(EncoderElement(MIDI_CC_TYPE,
                          channel, cc, macro_map_mode, name=name))

            if len(parameter_encoders_raw) > 0:
                layer_specs['parameter_controls'] = ButtonMatrixElement(rows=[
                 parameter_encoders_raw])
            device.layer = Layer(**layer_specs)
            self.set_device_component(device)

    def _init_transport_component(self, transport_controls, global_channel):

        def make_transport_button(control, name, is_momentary=True):
            return ButtonElement(is_momentary,
              MIDI_CC_TYPE,
              global_channel,
              (transport_controls[control]),
              name=name)

        if transport_controls:
            momentary_seek = 'NORELEASE' not in list(transport_controls.keys())
            layer_specs = {}
            if has_specification_for('STOP', transport_controls):
                layer_specs['stop_button'] = make_transport_button('STOP', 'Stop_Button')
            if has_specification_for('PLAY', transport_controls):
                layer_specs['play_button'] = make_transport_button('PLAY', 'Play_Button')
            if has_specification_for('REC', transport_controls):
                layer_specs['record_button'] = make_transport_button('REC', 'Record_Button')
            if has_specification_for('LOOP', transport_controls):
                layer_specs['loop_button'] = make_transport_button('LOOP', 'Loop_Button')
            if has_specification_for('FFWD', transport_controls):
                layer_specs['seek_forward_button'] = make_transport_button('FFWD',
                  'FFwd_Button', is_momentary=momentary_seek)
            if has_specification_for('RWD', transport_controls):
                layer_specs['seek_backward_button'] = make_transport_button('RWD',
                  'Rwd_Button', is_momentary=momentary_seek)
            transport = TransportComponent(name='Transport')
            transport.layer = Layer(**layer_specs)