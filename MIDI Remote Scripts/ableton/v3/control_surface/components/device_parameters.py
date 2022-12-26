from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import DeviceParameterComponent
from ..controls import MappedSensitivitySettingControl, control_list

class DeviceParametersComponent(DeviceParameterComponent):
    controls = control_list(MappedSensitivitySettingControl, 8)

    def __init__(self, name='Device_Parameters', is_private=True, *a, **k):
        (super().__init__)(a, name=name, **k)
        self.is_private = is_private

    def set_parameter_controls(self, encoders):
        if encoders:
            if len(encoders) > self.controls.control_count:
                self.controls.control_count = len(encoders)
        self.controls.set_control_element(encoders)
        self._connect_parameters()