from __future__ import absolute_import, print_function, unicode_literals
import re
import Live
AutomationState = Live.DeviceParameter.AutomationState
ModulationSource = Live.WavetableDevice.ModulationSource
ParameterState = Live.DeviceParameter.ParameterState
from ableton.v2.base import EventObject, find_if, listens, listenable_property, liveobj_valid
from ableton.v2.control_surface import Layer
from pushbase.actions import DeleteAndReturnToDefaultComponent
from pushbase.consts import MessageBoxText
from pushbase.decoration import LiveObjectDecorator
from pushbase.internal_parameter import EnumWrappingParameter, IntegerParameter, InternalParameter, InternalParameterBase
from .device_decoration import get_parameter_by_name, IndexProvider, ModMatrixParameter, NotifyingList, PitchParameter
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceTriggerOption, DeviceSwitchOption, DeviceOnOffOption
from .visualisation_settings import VisualisationGuides

class InstrumentVectorEnvelopeType(int):
    pass


InstrumentVectorEnvelopeType.amp = InstrumentVectorEnvelopeType(0)
InstrumentVectorEnvelopeType.env2 = InstrumentVectorEnvelopeType(1)
InstrumentVectorEnvelopeType.env3 = InstrumentVectorEnvelopeType(2)

class InstrumentVectorLfoType(int):
    pass


InstrumentVectorLfoType.one = InstrumentVectorLfoType(0)
InstrumentVectorLfoType.two = InstrumentVectorLfoType(1)

class InstrumentVectorEnvelopeViewType(int):
    pass


InstrumentVectorEnvelopeViewType.time = InstrumentVectorEnvelopeViewType(0)
InstrumentVectorEnvelopeViewType.slope = InstrumentVectorEnvelopeViewType(1)
InstrumentVectorEnvelopeViewType.value = InstrumentVectorEnvelopeViewType(2)

class InstrumentVectorOscillatorType(int):
    pass


InstrumentVectorOscillatorType.one = InstrumentVectorOscillatorType(0)
InstrumentVectorOscillatorType.two = InstrumentVectorOscillatorType(1)
InstrumentVectorOscillatorType.s = InstrumentVectorOscillatorType(2)
InstrumentVectorOscillatorType.mix = InstrumentVectorOscillatorType(3)

class InstrumentVectorFilterType(int):
    pass


InstrumentVectorFilterType.one = InstrumentVectorFilterType(0)
InstrumentVectorFilterType.two = InstrumentVectorFilterType(1)

class InstrumentVectorDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_UNISON_VOICE_COUNT = 2
    MAX_UNISON_VOICE_COUNT = 8
    available_effect_modes = (u'None',
     u'Fm',
     u'Classic',
     u'Modern')
    available_filter_curcuit_lp_hp_values = (u'Clean',
     u'OSR',
     u'MS2',
     u'SMP',
     u'PRD')
    available_filter_curcuit_bp_no_morph_values = (u'Clean', u'OSR')
    available_unison_modes = (u'None',
     u'Classic',
     u'Shimmer',
     u'Noise',
     u'Phase Sync',
     u'Position Spread',
     u'Random Note')
    mono_off_on_values = (u'Off', u'On')
    poly_voices_values = (u'2',
     u'3',
     u'4',
     u'5',
     u'6',
     u'7',
     u'8')
    available_filter_routings = (u'Serial', u'Parallel', u'Split')
    __events__ = (u'request_bank_view', u'request_previous_bank_from_mod_matrix')

    def __init__(self, *a, **k):
        super(InstrumentVectorDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = NotifyingList(available_values=[u'1',
         u'2',
         u'S',
         u'Mix'], default_value=InstrumentVectorOscillatorType.one)
        self._filter_types_provider = NotifyingList(available_values=[u'1', u'2'], default_value=InstrumentVectorFilterType.one)
        self._envelope_types_provider = NotifyingList(available_values=[u'Amp', u'Env2', u'Env3'], default_value=InstrumentVectorEnvelopeType.amp)
        self._lfo_types_provider = NotifyingList(available_values=[u'LFO1', u'LFO2'], default_value=InstrumentVectorLfoType.one)
        self._amp_envelope_view_types_provider = NotifyingList(available_values=[u'Time', u'Slope'], default_value=InstrumentVectorEnvelopeViewType.time)
        self._mod_envelope_view_types_provider = NotifyingList(available_values=[u'Time', u'Slope', u'Value'], default_value=InstrumentVectorEnvelopeViewType.time)
        self.current_mod_target_index = IndexProvider()
        self._single_selected_parameter = None
        self._additional_parameters = self._create_parameters()
        self._options = self._create_options()
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self._options)
        self.__on_oscillator_switch_value_changed.subject = self.oscillator_switch
        self.__on_internal_filter_switch_value_changed.subject = self.filter_switch_for_filter_switch_option
        self.__on_current_mod_target_index_changed.subject = self.current_mod_target_index
        self.__on_lfo_types_provider_index_changed.subject = self._lfo_types_provider
        self._osc_1_on_parameter = get_parameter_by_name(self, u'Osc 1 On')
        self._osc_2_on_parameter = get_parameter_by_name(self, u'Osc 2 On')
        self.__on_osc_1_on_value_changed.subject = self._osc_1_on_parameter
        self.__on_osc_1_on_value_changed()
        self.__on_osc_2_on_value_changed.subject = self._osc_2_on_parameter
        self.__on_osc_2_on_value_changed()
        self._filter_1_on_parameter = get_parameter_by_name(self, u'Filter 1 On')
        self._filter_2_on_parameter = get_parameter_by_name(self, u'Filter 2 On')
        self.__on_filter_1_on_value_changed.subject = self._filter_1_on_parameter
        self.__on_filter_1_on_value_changed()
        self.__on_filter_2_on_value_changed.subject = self._filter_2_on_parameter
        self.__on_filter_2_on_value_changed()

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._options

    @listenable_property
    def oscillator_index(self):
        return self._osc_types_provider.index

    @listenable_property
    def filter_index(self):
        return self._filter_types_provider.index

    @listenable_property
    def lfo_index(self):
        return self._lfo_types_provider.index

    @property
    def single_selected_parameter(self):
        return self._single_selected_parameter

    def set_single_selected_parameter(self, value):
        self._single_selected_parameter = value
        self.add_to_mod_matrix_option.notify_active()

    @listenable_property
    def current_mod_target_parameter(self):
        return self._get_current_mod_target_parameter()

    def _create_parameters(self):
        self.oscillator_switch = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorOscillatorType)
        self.osc_1_pitch = PitchParameter(name=u'Osc 1 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 1 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 1 Detune'))
        self.osc_2_pitch = PitchParameter(name=u'Osc 2 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 2 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 2 Detune'))
        self.filter_switch_for_filter_switch_option = EnumWrappingParameter(name=u'Internal Filter', parent=self, values_host=self._filter_types_provider, index_property_host=self._filter_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorFilterType)
        self.current_mod_target = InternalParameter(name=u'Current Mod Target', parent=self)
        self.envelope_switch = EnumWrappingParameter(name=u'Envelopes', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeType)
        self.lfo_switch = EnumWrappingParameter(name=u'LFO', parent=self, values_host=self._lfo_types_provider, index_property_host=self._lfo_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorLfoType)
        self._osc_1_category_switch = EnumWrappingParameter(name=u'Osc 1 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_1_wavetable_category')
        self._osc_2_category_switch = EnumWrappingParameter(name=u'Osc 2 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_2_wavetable_category')
        self._osc_1_table_switch = EnumWrappingParameter(name=u'Osc 1 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_1_wavetables', index_property=u'oscillator_1_wavetable_index')
        self._osc_2_table_switch = EnumWrappingParameter(name=u'Osc 2 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_2_wavetables', index_property=u'oscillator_2_wavetable_index')
        self._osc_1_effect_type_switch = EnumWrappingParameter(name=u'Osc 1 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_1_effect_mode')
        self._osc_2_effect_type_switch = EnumWrappingParameter(name=u'Osc 2 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_2_effect_mode')
        self._filter_1_circuit_lp_hp_switch = EnumWrappingParameter(name=u'Filter 1 Circuit LP/HP', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 1 LP/HP'), values_property=u'available_filter_curcuit_lp_hp_values', index_property=u'value')
        self._filter_2_circuit_lp_hp_switch = EnumWrappingParameter(name=u'Filter 2 Circuit LP/HP', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 2 LP/HP'), values_property=u'available_filter_curcuit_lp_hp_values', index_property=u'value')
        self._filter_1_circuit_bp_no_morph_switch = EnumWrappingParameter(name=u'Filter 1 Circuit BP/NO/Morph', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 1 BP/NO/Morph'), values_property=u'available_filter_curcuit_bp_no_morph_values', index_property=u'value')
        self._filter_2_circuit_bp_no_morph_switch = EnumWrappingParameter(name=u'Filter 2 Circuit BP/NO/Morph', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 2 BP/NO/Morph'), values_property=u'available_filter_curcuit_bp_no_morph_values', index_property=u'value')
        return (EnumWrappingParameter(name=u'Filter', parent=self, values_host=self._filter_types_provider, index_property_host=self._filter_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorFilterType),
         EnumWrappingParameter(name=u'Amp Env View', parent=self, values_host=self._amp_envelope_view_types_provider, index_property_host=self._amp_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeViewType),
         EnumWrappingParameter(name=u'Mod Env View', parent=self, values_host=self._mod_envelope_view_types_provider, index_property_host=self._mod_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeViewType),
         EnumWrappingParameter(name=u'Modulation Target Names', parent=self, values_host=self._live_object, index_property_host=self.current_mod_target_index, values_property=u'visible_modulation_target_names', index_property=u'index'),
         ModMatrixParameter(name=u'Amp Env Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.amp_envelope),
         ModMatrixParameter(name=u'Env 2 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.envelope_2),
         ModMatrixParameter(name=u'Env 3 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.envelope_3),
         ModMatrixParameter(name=u'Lfo 1 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.lfo_1),
         ModMatrixParameter(name=u'Lfo 2 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.lfo_2),
         ModMatrixParameter(name=u'MIDI Velocity Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_velocity),
         ModMatrixParameter(name=u'MIDI Note Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_note),
         ModMatrixParameter(name=u'MIDI Pitch Bend Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_pitch_bend),
         ModMatrixParameter(name=u'MIDI Aftertouch Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_channel_pressure),
         ModMatrixParameter(name=u'MIDI Mod Wheel Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_mod_wheel),
         EnumWrappingParameter(name=u'Unison Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_unison_modes', index_property=u'unison_mode'),
         IntegerParameter(name=u'Unison Voices', parent=self, integer_value_host=self._live_object, integer_value_property_name=u'unison_voice_count', min_value=self.MIN_UNISON_VOICE_COUNT, max_value=self.MAX_UNISON_VOICE_COUNT, show_as_quantized=True),
         EnumWrappingParameter(name=u'Mono On', parent=self, values_host=self, index_property_host=self, values_property=u'mono_off_on_values', index_property=u'mono_poly', to_index_conversion=lambda index: int(not index), from_index_conversion=lambda index: int(not index)),
         EnumWrappingParameter(name=u'Poly Voices', parent=self, values_host=self, index_property_host=self, values_property=u'poly_voices_values', index_property=u'poly_voices'),
         EnumWrappingParameter(name=u'Filter Routing', parent=self, values_host=self, index_property_host=self, values_property=u'available_filter_routings', index_property=u'filter_routing')) + (self.oscillator_switch,
         self.osc_1_pitch,
         self.osc_2_pitch,
         self.filter_switch_for_filter_switch_option,
         self.current_mod_target,
         self.envelope_switch,
         self.lfo_switch,
         self._osc_1_category_switch,
         self._osc_2_category_switch,
         self._osc_1_table_switch,
         self._osc_2_table_switch,
         self._osc_1_effect_type_switch,
         self._osc_2_effect_type_switch,
         self._filter_1_circuit_lp_hp_switch,
         self._filter_2_circuit_lp_hp_switch,
         self._filter_1_circuit_bp_no_morph_switch,
         self._filter_2_circuit_bp_no_morph_switch)

    def _create_options(self):

        def is_selected_parameter_modulatable():
            if self.single_selected_parameter is None:
                return False
            if isinstance(self.single_selected_parameter, PitchParameter):
                return True
            if isinstance(self.single_selected_parameter, InternalParameterBase):
                return False
            return self._live_object.is_parameter_modulatable(self.single_selected_parameter)

        def add_selected_parameter_to_mod_matrix():
            if is_selected_parameter_modulatable():
                param = self.single_selected_parameter.decimal_value_host if isinstance(self.single_selected_parameter, PitchParameter) else self.single_selected_parameter
                self.current_mod_target_index.index = self._live_object.add_parameter_to_modulation_matrix(param)
                self.notify_request_bank_view(u'Matrix')

        def jump_to_bank(bank_name):
            self.notify_request_bank_view(bank_name)

        def choose_envelope(value):
            self.envelope_switch.value = value

        def choose_lfo(value):
            self.lfo_switch.value = value

        self.osc_on_option = DeviceOnOffOption(name=u'Osc', property_host=self._get_osc_on_property_host())
        self.filter_on_option = DeviceOnOffOption(name=u'Filter', property_host=self._get_filter_on_property_host())
        self.lfo_retrigger_option = DeviceOnOffOption(name=u'Retrigger', property_host=self._get_lfo_retrigger_property_host())
        self.add_to_mod_matrix_option = DeviceTriggerOption(name=u'Add to Matrix', callback=add_selected_parameter_to_mod_matrix, is_active=is_selected_parameter_modulatable)
        return (DeviceOnOffOption(name=u'Sub', property_host=get_parameter_by_name(self, u'Sub On')),
         DeviceSwitchOption(name=u'Filter 1 Slope', parameter=get_parameter_by_name(self, u'Filter 1 Slope'), labels=[u'12dB', u'24dB']),
         DeviceSwitchOption(name=u'Filter 2 Slope', parameter=get_parameter_by_name(self, u'Filter 2 Slope'), labels=[u'12dB', u'24dB']),
         DeviceSwitchOption(name=u'Filter Switch', parameter=self.filter_switch_for_filter_switch_option, labels=[u'Filter 1', u'Filter 2']),
         DeviceSwitchOption(name=u'LFO 1 Sync', parameter=get_parameter_by_name(self, u'LFO 1 Sync'), labels=[u'Hz', u'Sync']),
         DeviceSwitchOption(name=u'LFO 2 Sync', parameter=get_parameter_by_name(self, u'LFO 2 Sync'), labels=[u'Hz', u'Sync']),
         DeviceTriggerOption(name=u'Go to Amp Env', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.amp), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to Env 2', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.env2), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to Env 3', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.env3), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to LFO 1', callback=lambda : (choose_lfo(InstrumentVectorLfoType.one), jump_to_bank(u'LFOs'))),
         DeviceTriggerOption(name=u'Go to LFO 2', callback=lambda : (choose_lfo(InstrumentVectorLfoType.two), jump_to_bank(u'LFOs'))),
         DeviceTriggerOption(name=u'Back', callback=self.notify_request_previous_bank_from_mod_matrix)) + (self.osc_on_option,
         self.filter_on_option,
         self.lfo_retrigger_option,
         self.add_to_mod_matrix_option)

    def _get_parameter_by_name(self, name):
        return find_if(lambda p: p.name == name, self.parameters)

    def _get_osc_on_property_host(self):
        return get_parameter_by_name(self, u'Osc {} On'.format(2 if self.oscillator_switch.value else 1))

    def _get_filter_on_property_host(self):
        return get_parameter_by_name(self, u'Filter {} On'.format(self.filter_switch_for_filter_switch_option.value + 1))

    def _get_lfo_retrigger_property_host(self):
        return get_parameter_by_name(self, u'LFO {} Retrigger'.format(self._lfo_types_provider.index + 1))

    def _resolve_ambiguous_modulation_target_name(self, target_parameter_name):
        if re.match(u'^Osc (1|2) Transp$', target_parameter_name):
            return target_parameter_name.replace(u'Transp', u'Pitch')
        lfo_rate_re = re.match(u'^LFO (1|2) S\\. Rate$', target_parameter_name)
        if lfo_rate_re:
            lfo_number = lfo_rate_re.group(1)
            lfo_sync_param = get_parameter_by_name(self, u'LFO {} Sync'.format(lfo_number))
            if lfo_sync_param.value == 0:
                return u'LFO {} Rate'.format(lfo_number)
        return target_parameter_name

    def _get_current_mod_target_parameter(self):
        target_parameter_name = self._resolve_ambiguous_modulation_target_name(self.get_modulation_target_parameter_name(self.current_mod_target_index.index))
        return self._get_parameter_by_name(target_parameter_name)

    def _get_parameter_enabled_state(self, parameter):
        if parameter.value:
            return ParameterState.enabled
        return ParameterState.disabled

    @listens(u'value')
    def __on_oscillator_switch_value_changed(self):
        self.osc_on_option.set_property_host(self._get_osc_on_property_host())
        self.notify_oscillator_index()

    @listens(u'value')
    def __on_internal_filter_switch_value_changed(self):
        self.filter_on_option.set_property_host(self._get_filter_on_property_host())
        self.notify_filter_index()

    @listens(u'index')
    def __on_current_mod_target_index_changed(self):
        self.notify_current_mod_target_parameter()

    @listens(u'index')
    def __on_lfo_types_provider_index_changed(self):
        self.lfo_retrigger_option.set_property_host(self._get_lfo_retrigger_property_host())
        self.notify_lfo_index()

    @listens(u'value')
    def __on_osc_1_on_value_changed(self):
        if liveobj_valid(self._osc_1_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_1_on_parameter)
            self._osc_1_category_switch.state = state
            self._osc_1_table_switch.state = state
            self._osc_1_effect_type_switch.state = state
            self.osc_1_pitch.state = state

    @listens(u'value')
    def __on_osc_2_on_value_changed(self):
        if liveobj_valid(self._osc_2_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_2_on_parameter)
            self._osc_2_category_switch.state = state
            self._osc_2_table_switch.state = state
            self._osc_2_effect_type_switch.state = state
            self.osc_2_pitch.state = state

    @listens(u'value')
    def __on_filter_1_on_value_changed(self):
        if liveobj_valid(self._filter_1_on_parameter):
            state = self._get_parameter_enabled_state(self._filter_1_on_parameter)
            self._filter_1_circuit_lp_hp_switch.state = state
            self._filter_1_circuit_bp_no_morph_switch.state = state

    @listens(u'value')
    def __on_filter_2_on_value_changed(self):
        if liveobj_valid(self._filter_2_on_parameter):
            state = self._get_parameter_enabled_state(self._filter_2_on_parameter)
            self._filter_2_circuit_lp_hp_switch.state = state
            self._filter_2_circuit_bp_no_morph_switch.state = state


def has_automation(parameter):
    return parameter.automation_state != AutomationState.none


class InstrumentVectorDeleteComponent(DeleteAndReturnToDefaultComponent):

    def delete_clip_envelope(self, parameter):
        if isinstance(parameter, PitchParameter) and has_automation(parameter):
            playing_clip = self._get_playing_clip()
            if playing_clip:
                deleted_automation_names = []
                for parameter in [parameter.integer_value_host, parameter.decimal_value_host]:
                    if has_automation(parameter):
                        playing_clip.clear_envelope(parameter)
                        deleted_automation_names.append(parameter.name)

                if deleted_automation_names:
                    self.show_notification(MessageBoxText.DELETE_ENVELOPE % dict(automation=u', '.join(deleted_automation_names)))
        else:
            super(InstrumentVectorDeleteComponent, self).delete_clip_envelope(parameter)


class InstrumentVectorDeviceComponent(DeviceComponentWithTrackColorViewData):
    OSCILLATOR_POSITION_PARAMETER_NAMES = re.compile(u'^(Osc (1|2) Pos)$|^Position$')
    FILTER_PARAMETER_NAMES = re.compile(u'^(Filter (1|2) (Type|Freq|Res))$|^Filter Type$|^Frequency$|^Resonance$')
    LFO_PARAMETER_NAMES = re.compile(u'^(LFO (1|2) (Shape|Shaping|S. Rate|Rate|Amount|Attack Time|Phase Offset))$|^LFO$|^LFO Type$|^Shape$|^Rate$|^Amount$|^Attack$|^Offset$')
    WAVETABLE_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(0, 2),
     1: ButtonRange(1, 3)}
    FILTER_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(3, 5),
     2: ButtonRange(2, 4)}
    LFO_VISUALISATION_CONFIGURATION_IN_BANKS = {5: ButtonRange(0, 3)}

    def __init__(self, *a, **k):
        super(InstrumentVectorDeviceComponent, self).__init__(*a, **k)
        self._bank_before_mod_matrix = 0
        self._delete_default_component = self.register_component(InstrumentVectorDeleteComponent(name=u'DeleteAndDefault'))
        self._delete_default_component.layer = Layer(delete_button=self._delete_button)

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            if self._is_resetting_parameter() and self._is_custom_parameter(parameter):
                self._delete_default_component.delete_clip_envelope(parameter)
            view_data = {}
            self._update_single_selected_parameter()
            if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingPosition'] = True
            if self.FILTER_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingFilter'] = True
            if self.LFO_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingLfo'] = True
            if view_data:
                self._update_visualisation_view_data(view_data)

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            view_data = {}
            self._update_single_selected_parameter()
            if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingPosition'] = False
            if not self._any_filter_parameter_touched():
                view_data[u'AdjustingFilter'] = False
            if not self._any_lfo_parameter_touched():
                view_data[u'AdjustingLfo'] = False
            if view_data:
                self._update_visualisation_view_data(view_data)

    def _is_resetting_parameter(self):
        return self._delete_default_component is not None and self._delete_default_component.is_deleting

    def _is_custom_parameter(self, parameter):
        return isinstance(parameter, ModMatrixParameter) or isinstance(parameter, PitchParameter)

    def _get_provided_parameters(self):
        _, parameters = self._current_bank_details() if self.device() else (None, ())
        provided_parameters = []
        for param, name in parameters:
            if param == self._decorated_device.current_mod_target:
                param = self._decorated_device.current_mod_target_parameter
                name = param.name if param is not None else u''
            provided_parameters.append(self._create_parameter_info(param, name))

        return provided_parameters

    def _shift_button_pressed(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = True
        self._decorated_device.osc_2_pitch.adjust_finegrain = True

    def _shift_button_released(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = False
        self._decorated_device.osc_2_pitch.adjust_finegrain = False

    def _set_decorated_device(self, decorated_device):
        super(InstrumentVectorDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_oscillator_changed.subject = decorated_device
        self.__on_selected_filter_changed.subject = decorated_device
        self.__on_selected_lfo_changed.subject = decorated_device
        self.__on_request_bank_view.subject = decorated_device
        self.__on_request_previous_bank_from_mod_matrix.subject = decorated_device
        self.__on_current_mod_target_parameter_changed.subject = decorated_device

    def _set_bank_index(self, bank):
        current_bank = self._bank.index
        bank_definition = self._banking_info.device_bank_definition(self.device())
        if bank_definition.key_by_index(current_bank) not in (u'Matrix', u'MIDI'):
            self._bank_before_mod_matrix = current_bank
        super(InstrumentVectorDeviceComponent, self)._set_bank_index(bank)
        self._update_single_selected_parameter()
        self._update_visualisation_view_data(self._get_current_view_data())
        self.notify_visualisation_visible()
        self.notify_wavetable_visualisation_visible()
        self.notify_filter_visualisation_visible()
        self.notify_lfo_visualisation_visible()
        self.notify_shrink_parameters()

    def _update_single_selected_parameter(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        self._decorated_device.set_single_selected_parameter(touched_parameters[0].parameter if len(touched_parameters) == 1 else None)

    def _any_filter_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ self.FILTER_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters ])

    def _any_lfo_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ self.LFO_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters ])

    @property
    def _visualisation_visible(self):
        return self.wavetable_visualisation_visible or self.filter_visualisation_visible or self.lfo_visualisation_visible

    @listenable_property
    def wavetable_visualisation_visible(self):
        return self._bank.index in self.WAVETABLE_VISUALISATION_CONFIGURATION_IN_BANKS and self.selected_oscillator in [InstrumentVectorOscillatorType.one, InstrumentVectorOscillatorType.two]

    @listenable_property
    def filter_visualisation_visible(self):
        return self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS

    @listenable_property
    def lfo_visualisation_visible(self):
        return self._bank.index in self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS

    @property
    def selected_oscillator(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.oscillator_index
        return 0

    @property
    def selected_filter(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.filter_index
        return 0

    @property
    def selected_lfo(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.lfo_index
        return 0

    @property
    def visualisation_width(self):
        return VisualisationGuides.light_right_x(2) - VisualisationGuides.light_left_x(0)

    def _get_wavetable_visualisation_range(self):
        return self.WAVETABLE_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(0, 0))

    def _get_filter_visualisation_range(self):
        return self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(0, 0))

    def _get_lfo_visualisation_range(self):
        return self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(0, 0))

    @property
    def _shrink_parameters(self):
        if self.visualisation_visible:
            wavetable_visualisation_range = self._get_wavetable_visualisation_range()
            filter_visualisation_range = self._get_filter_visualisation_range()
            lfo_visualisation_range = self._get_lfo_visualisation_range()

            def is_shrunk(index):
                return self.wavetable_visualisation_visible and wavetable_visualisation_range.left_index <= index <= wavetable_visualisation_range.right_index or self.filter_visualisation_visible and filter_visualisation_range.left_index <= index <= filter_visualisation_range.right_index or self.lfo_visualisation_visible and lfo_visualisation_range.left_index <= index <= lfo_visualisation_range.right_index

            return [ is_shrunk(parameter_index) for parameter_index in range(8) ]
        return [False] * 8

    def _initial_visualisation_view_data(self):
        view_data = super(InstrumentVectorDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._get_current_view_data())
        return view_data

    def _get_current_view_data(self):
        lfo_visualisation_range = self._get_lfo_visualisation_range()
        return {u'SelectedOscillator': self.selected_oscillator,
         u'AdjustingPosition': False,
         u'AdjustingFilter': False,
         u'AdjustingLfo': False,
         u'WavetableVisualisationStart': VisualisationGuides.light_left_x(self._get_wavetable_visualisation_range().left_index),
         u'WavetableVisualisationWidth': self.visualisation_width,
         u'FilterCurveVisualisationStart': VisualisationGuides.light_left_x(self._get_filter_visualisation_range().left_index),
         u'FilterCurveVisualisationWidth': self.visualisation_width,
         u'LfoVisualisationStart': VisualisationGuides.light_left_x(lfo_visualisation_range.left_index),
         u'LfoVisualisationWidth': VisualisationGuides.light_right_x(lfo_visualisation_range.right_index) - VisualisationGuides.light_left_x(lfo_visualisation_range.left_index),
         u'WavetableVisualisationVisible': self.wavetable_visualisation_visible,
         u'FilterVisualisationVisible': self.filter_visualisation_visible,
         u'LfoVisualisationVisible': self.lfo_visualisation_visible,
         u'SelectedFilter': self.selected_filter,
         u'SelectedLfo': self.selected_lfo}

    @listens(u'request_bank_view')
    def __on_request_bank_view(self, bank_name):
        device = self.device()
        bank_definition = self._banking_info.device_bank_definition(device)
        if bank_name in bank_definition:
            self._device_bank_registry.set_device_bank(device, bank_definition.index_by_key(bank_name))

    @listens(u'request_previous_bank_from_mod_matrix')
    def __on_request_previous_bank_from_mod_matrix(self):
        self._device_bank_registry.set_device_bank(self.device(), self._bank_before_mod_matrix)

    @listens(u'oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data({u'SelectedOscillator': self.selected_oscillator,
         u'WavetableVisualisationVisible': self.wavetable_visualisation_visible})
        self.notify_visualisation_visible()
        self.notify_wavetable_visualisation_visible()
        self.notify_shrink_parameters()

    @listens(u'filter_index')
    def __on_selected_filter_changed(self):
        self._update_visualisation_view_data({u'SelectedFilter': self.selected_filter})

    @listens(u'lfo_index')
    def __on_selected_lfo_changed(self):
        self._update_visualisation_view_data({u'SelectedLfo': self.selected_lfo})

    @listens(u'current_mod_target_parameter')
    def __on_current_mod_target_parameter_changed(self):
        self._update_parameters()
