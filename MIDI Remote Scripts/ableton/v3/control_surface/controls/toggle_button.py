from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.control as ToggleButtonControlBase

class ToggleButtonControl(ToggleButtonControlBase):

    class State(ToggleButtonControlBase.State):

        def on_connected_property_changed(self, value=None):
            self.is_toggled = value or self.connected_property_value