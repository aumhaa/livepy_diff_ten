from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import MultiElement as MultiElementBase

class MultiElement(MultiElementBase):

    def __init__(self, *a, **k):
        super(MultiElement, self).__init__(*a, **k)
        self._parameter_to_map_to = None

    @property
    def touch_element(self):
        for control in self.owned_control_elements():
            if hasattr(control, u'touch_element'):
                return control.touch_element

    def connect_to(self, parameter):
        self._parameter_to_map_to = parameter
        for control in self.owned_control_elements():
            control.connect_to(parameter)

    def release_parameter(self):
        self._parameter_to_map_to = None
        for control in self.owned_control_elements():
            control.release_parameter()

    def mapped_parameter(self):
        return self._parameter_to_map_to
