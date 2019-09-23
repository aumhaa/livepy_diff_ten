from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from _Generic.Devices import best_of_parameter_bank
from ableton.v2.base import depends, EventObject, listens, liveobj_valid, nop
from ableton.v2.control_surface import Component

def release_control(control):
    if liveobj_valid(control):
        control.release_parameter()


class SimpleDeviceParameterComponent(Component):

    @depends(device_provider=None)
    def __init__(self, device_provider = None, *a, **k):
        super(SimpleDeviceParameterComponent, self).__init__(*a, **k)
        self._device = None
        self._parameter_controls = None
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self._device_provider = device_provider
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()

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
        self.update()

    def update(self):
        super(SimpleDeviceParameterComponent, self).update()
        if self.is_enabled():
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
        bank = best_of_parameter_bank(self._device)
        for control, parameter in izip_longest(self._parameter_controls or [], bank):
            if liveobj_valid(control):
                if liveobj_valid(parameter):
                    control.connect_to(parameter)
                else:
                    control.release_parameter()
