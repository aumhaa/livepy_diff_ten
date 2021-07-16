from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl

class LightingComponent(Component):
    shift_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')
    zoom_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')