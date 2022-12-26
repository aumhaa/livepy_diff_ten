from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as DeviceComponentBase
from ableton.v3.control_surface.parameter_info import ParameterInfo
from ...base import depends, find_if, listens, liveobj_valid
from .. import DEFAULT_BANK_SIZE, BankingInfo, create_parameter_bank, legacy_bank_definitions
from ..controls import MappedButtonControl, ToggleButtonControl
from ..default_bank_definitions import BANK_DEFINITIONS
from ..device_decorators import DeviceDecoratorFactory
from ..parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameter_mapping_sensitivities
from .device_bank_navigation import DeviceBankNavigationComponent
from .device_parameters import DeviceParametersComponent

def get_on_off_parameter(device):
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled, device.parameters)


class DeviceComponent(DeviceComponentBase):
    device_on_off_button = MappedButtonControl(color='Device.Off', on_color='Device.On')
    device_lock_button = ToggleButtonControl(untoggled_color='Device.LockOff',
      toggled_color='Device.LockOn')

    @depends(device_bank_registry=None, toggle_lock=None, show_message=None)
    def __init__(self, name='Device', continuous_parameter_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, quantized_parameter_sensitivity=DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameters_component_type=None, bank_size=DEFAULT_BANK_SIZE, bank_definitions=None, bank_navigation_component_type=None, device_bank_registry=None, device_decorator_factory=None, toggle_lock=None, show_message=None, is_private=True, *a, **k):
        self._parameter_mapping_sensitivities = parameter_mapping_sensitivities(continuous_parameter_sensitivity=continuous_parameter_sensitivity,
          quantized_parameter_sensitivity=quantized_parameter_sensitivity)
        parameters_component_type = parameters_component_type or DeviceParametersComponent
        self._parameters_component = parameters_component_type()
        self._parameters_component.parameter_provider = self
        banking_info = BankingInfo((bank_definitions or BANK_DEFINITIONS),
          bank_size=bank_size)
        bank_navigation_component_type = bank_navigation_component_type or DeviceBankNavigationComponent
        self._bank_navigation_component = bank_navigation_component_type(banking_info=banking_info,
          device_bank_registry=device_bank_registry)
        (super().__init__)(a, name=name, banking_info=banking_info, device_bank_registry=device_bank_registry, device_decorator_factory=device_decorator_factory or DeviceDecoratorFactory() if bank_definitions not in [legacy_bank_definitions.banked(), legacy_bank_definitions.best_of_banks()] else None, **k)
        self.is_private = is_private
        self._toggle_lock = toggle_lock
        self._show_message = show_message
        self.add_children(self._parameters_component, self._bank_navigation_component)
        self.register_slot(self._device_provider, self._update_device_lock_button, 'is_locked_to_device')
        self._update_device_lock_button()

    def set_parameter_controls(self, controls):
        self._parameters_component.set_parameter_controls(controls)

    def __getattr__(self, name):
        if name.startswith('set_'):
            if 'bank' in name:
                return getattr(self._bank_navigation_component, name)
        raise AttributeError

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._toggle_lock()

    def _create_parameter_info(self, parameter, name):
        default, fine_grain = self._parameter_mapping_sensitivities(parameter, self.device())
        return ParameterInfo(parameter=parameter,
          name=name,
          default_encoder_sensitivity=default,
          fine_grain_encoder_sensitivity=fine_grain)

    def _set_device(self, device):
        super()._set_device(device)
        self.device_on_off_button.mapped_parameter = get_on_off_parameter(device)

    def _setup_bank(self, device, bank_factory=create_parameter_bank):
        super()._setup_bank(device, bank_factory=bank_factory)
        self._DeviceComponent__on_provider_bank_changed.subject = self._bank
        self._bank_navigation_component.bank_provider = self._bank

    def _set_bank_index(self, bank):
        super()._set_bank_index(bank)
        device = self.device()
        if liveobj_valid(device):
            if self._parameters_component.controls[0].control_element:
                self._show_message('Controlling {}: {}'.format(device.name, self._current_bank_details()[0]))

    @listens('parameters')
    def __on_provider_bank_changed(self):
        self._device_bank_registry.set_device_bank(self.device(), self._bank.index)

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device