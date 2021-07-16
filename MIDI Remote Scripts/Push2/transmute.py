from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import EventObject
from ableton.v2.control_surface import EnumWrappingParameter, IntegerParameter, LiveObjectDecorator, NotifyingList, get_parameter_by_name, WrappingParameter
from .device_decoration import DeviceOnOffOption, DeviceSwitchOption
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class TransmuteDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_PITCH_BEND_RANGE = 0
    MAX_PITCH_BEND_RANGE = 24
    polyphony_values = ('2', '4', '8', '16')

    def __init__(self, *a, **k):
        (super(TransmuteDeviceDecorator, self).__init__)(*a, **k)
        self.frequency_dial_mode = EnumWrappingParameter(name='Frequency Dial Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='frequency_dial_mode_list',
          index_property='frequency_dial_mode_index')
        self.midi_gate = EnumWrappingParameter(name='Midi Gate',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='midi_gate_list',
          index_property='midi_gate_index')
        self.mod_mode = EnumWrappingParameter(name='Mod Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='mod_mode_list',
          index_property='mod_mode_index')
        self.mono_poly = EnumWrappingParameter(name='Mono Poly',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='mono_poly_list',
          index_property='mono_poly_index')
        self.pitch_mode = EnumWrappingParameter(name='Pitch Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='pitch_mode_list',
          index_property='pitch_mode_index')
        self.pitch_bend_range_parameter = IntegerParameter(name='Pitch Bend Range',
          parent=self,
          integer_value_host=(self._live_object),
          integer_value_property_name='pitch_bend_range',
          min_value=(self.MIN_PITCH_BEND_RANGE),
          max_value=(self.MAX_PITCH_BEND_RANGE),
          show_as_quantized=False)
        self.polyphony_parameter = EnumWrappingParameter(name='Polyphony',
          parent=self,
          values_host=self,
          index_property_host=self,
          values_property='polyphony_values',
          index_property='polyphony')
        self._additional_parameters = (
         self.frequency_dial_mode,
         self.midi_gate,
         self.mod_mode,
         self.mono_poly,
         self.pitch_mode,
         self.pitch_bend_range_parameter,
         self.polyphony_parameter)
        self.freq_dial_mode_option = DeviceSwitchOption(name='frequency_dial_mode_opt',
          parameter=(self.frequency_dial_mode),
          labels=[
         'Hz', 'Note'])
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.freq_dial_mode_option,)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters