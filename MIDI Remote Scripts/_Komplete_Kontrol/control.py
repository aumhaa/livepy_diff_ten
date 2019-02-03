from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import Control, EncoderControl

class SendValueMixin(object):

    def __init__(self, *a, **k):
        super(SendValueMixin, self).__init__(*a, **k)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value != value:
            self._value = value
            self._send_current_value()

    def set_control_element(self, control_element):
        super(SendValueMixin, self).set_control_element(control_element)
        self._send_current_value()

    def update(self):
        super(SendValueMixin, self).update()
        self._send_current_value()

    def _send_current_value(self):
        if self._control_element:
            self._control_element.send_value(self._value)


class SendValueControl(Control):

    def __init__(self, *a, **k):
        super(SendValueControl, self).__init__(*a, **k)

    class State(SendValueMixin, Control.State):
        pass


class SendValueEncoderControl(EncoderControl):

    def __init__(self, *a, **k):
        super(SendValueEncoderControl, self).__init__(*a, **k)

    class State(SendValueMixin, EncoderControl.State):
        pass
