from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from _Generic.Devices import best_of_parameter_bank, parameter_banks
from ableton.v2.base import clamp, depends, EventObject, listens, liveobj_valid, nop
from ableton.v2.control_surface import Component

def release_control(control):
    if liveobj_valid(control):
        control.release_parameter()


class SimpleDeviceParameterComponent(Component):

    @depends(device_provider=None)
    def __init__(self, device_provider = None, use_parameter_banks = False, *a, **k):
        super(SimpleDeviceParameterComponent, self).__init__(*a, **k)
        self._use_parameter_banks = use_parameter_banks
        self._device = None
        self._banks = []
        self._bank_index = 0
        self._parameter_controls = None
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self._device_provider = device_provider
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()

    @property
    def bank_index(self):
        if self._use_parameter_banks:
            return self._bank_index
        return 0

    @bank_index.setter
    def bank_index(self, value):
        self._bank_index = self._clamp_to_bank_size(value)
        self.update()

    def _clamp_to_bank_size(self, value):
        return clamp(value, 0, self.num_banks - 1)

    @property
    def selected_bank(self):
        if self.num_banks:
            return self._banks[self._bank_index or 0]
        return []

    @property
    def num_banks(self):
        return len(self._banks)

    def set_parameter_controls(self, controls):
        for control in self._parameter_controls or []:
            release_control(control)

        self._parameter_controls = controls
        self.update()

    @listens(u'device')
    def __on_provided_device_changed(self):
        for control in self._parameter_controls or []:
            release_control(control)

        self._device = self._device_provider.device
        self.bank_index = 0

    def update(self):
        super(SimpleDeviceParameterComponent, self).update()
        if self.is_enabled():
            self._update_parameter_banks()
            self._empty_control_slots.disconnect()
            if liveobj_valid(self._device):
                self._connect_parameters()
            else:
                self._disconnect_parameters()
        else:
            self._disconnect_parameters()

    def _disconnect_parameters(self):
        for control in self._parameter_controls or []:
            release_control(control)
            self._empty_control_slots.register_slot(control, nop, u'value')

    def _connect_parameters(self):
        for control, parameter in izip_longest(self._parameter_controls or [], self.selected_bank):
            if liveobj_valid(control):
                if liveobj_valid(parameter):
                    control.connect_to(parameter)
                else:
                    control.release_parameter()
                    self._empty_control_slots.register_slot(control, nop, u'value')

    def _update_parameter_banks(self):
        if liveobj_valid(self._device):
            if self._use_parameter_banks:
                self._banks = parameter_banks(self._device)
            else:
                self._banks = [best_of_parameter_bank(self._device)]
        else:
            self._banks = []
        self._bank_index = self._clamp_to_bank_size(self._bank_index)
