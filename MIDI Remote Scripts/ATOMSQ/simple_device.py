from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import liveobj_valid, task
from ableton.v3.control_surface.components import DeviceComponent
from .control import DisplayControl
BANK_NAME_DISPLAY_DURATION = 1

class SimpleDeviceParameterComponent(DeviceComponent):
    device_name_display = DisplayControl()

    def __init__(self, *a, **k):
        self._device_name_slot = None
        (super().__init__)(a, force_use_parameter_banks=True, **k)
        self._device_name_slot = self.register_slot(self._device, self._update_device_name_display, 'name')
        self._display_bank_name_task = self._tasks.add(task.sequence(task.run(self._display_bank_name), task.wait(BANK_NAME_DISPLAY_DURATION), task.run(self._update_device_name_display)))
        self._display_bank_name_task.kill()

    @DeviceComponent.bank_index.setter
    def bank_index(self, value):
        if value != self._bank_index:
            self._display_bank_name_task.restart()
        super(SimpleDeviceParameterComponent, self.__class__).bank_index.fset(self, value)

    def update(self):
        super().update()
        if self._device_name_slot:
            self._device_name_slot.subject = self._device
        self._update_device_name_display()

    def _update_device_name_display(self):
        self.device_name_display.message = self._device.name if liveobj_valid(self._device) else ' - '

    def _display_bank_name(self):
        self.device_name_display.message = self._get_bank_name()