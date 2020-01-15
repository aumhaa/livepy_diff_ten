from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.control import ControlList, SendValueControl
from novation.launchpad_elements import SESSION_WIDTH
from novation.simple_device import SimpleDeviceParameterComponent as SimpleDeviceParameterComponentBase
from .control import SendReceiveValueControl
from .fixed_radio_button_group import FixedRadioButtonGroup
DEVICE_FADER_BANK = 3

class SimpleDeviceParameterComponent(SimpleDeviceParameterComponentBase):
    static_color_controls = ControlList(SendValueControl, 8)
    bank_select_buttons = FixedRadioButtonGroup(control_count=8, unchecked_color=u'Mode.Device.Bank.Available', checked_color=u'Mode.Device.Bank.Selected')
    stop_fader_control = SendReceiveValueControl()

    def __init__(self, static_color_value = 0, *a, **k):
        self._static_color_value = static_color_value
        super(SimpleDeviceParameterComponent, self).__init__(use_parameter_banks=True, *a, **k)
        self._update_static_color_controls()
        self._next_bank_index = self.bank_index

    @bank_select_buttons.checked
    def bank_select_buttons(self, button):
        self.stop_fader_control.send_value(DEVICE_FADER_BANK)
        self._next_bank_index = button.index

    @stop_fader_control.value
    def stop_fader_control(self, value, _):
        self.bank_index = self._next_bank_index

    def _update_parameter_banks(self):
        super(SimpleDeviceParameterComponent, self)._update_parameter_banks()
        self.bank_select_buttons.active_control_count = self.num_banks
        if self.bank_index < self.num_banks:
            self.bank_select_buttons[self.bank_index].is_checked = True

    def update(self):
        super(SimpleDeviceParameterComponent, self).update()
        self._update_static_color_controls()

    def _update_static_color_controls(self):
        if liveobj_valid(self._device) and self.selected_bank:
            for control, param in izip_longest(self.static_color_controls, self.selected_bank):
                color = self._static_color_value if liveobj_valid(param) else 0
                control.value = color

        else:
            for control in self.static_color_controls:
                control.value = 0
