from __future__ import absolute_import, print_function, unicode_literals
from .control import InputControl

class MappedControl(InputControl):
    u"""
    Control that is mapped to a parameter in Live.
    """

    class State(InputControl.State):
        u"""
        State-full representation of the Control.
        """

        def __init__(self, control = None, manager = None, *a, **k):
            assert control is not None
            assert manager is not None
            super(MappedControl.State, self).__init__(control=control, manager=manager, *a, **k)
            self._direct_mapping = None

        def set_control_element(self, control_element):
            u"""
            Connects the given Control Element with the Control. It will be mapped
            to the :attr:`mapped_parameter` in Live and follow the same rules as
            Live's MIDI mapping mechanism.
            """
            if self._control_element:
                self._control_element.release_parameter()
            super(MappedControl.State, self).set_control_element(control_element)
            self._update_direct_connection()

        @property
        def mapped_parameter(self):
            u"""
            The parameter that is controlled. Depending on the parameter, a different
            Control Element might be suited.
            """
            return self._direct_mapping

        @mapped_parameter.setter
        def mapped_parameter(self, direct_mapping):
            self._direct_mapping = direct_mapping
            self._update_direct_connection()

        def _update_direct_connection(self):
            if self._control_element:
                self._control_element.connect_to(self._direct_mapping)

        def _notifications_enabled(self):
            return super(MappedControl.State, self)._notifications_enabled() and self._direct_mapping is None

    def __init__(self, *a, **k):
        super(MappedControl, self).__init__(extra_args=a, extra_kws=k)
