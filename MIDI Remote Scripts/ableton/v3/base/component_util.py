from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ScrollComponent
from ableton.v2.control_surface.control import EncoderControl

def skin_scroll_buttons(component, color, pressed_color):
    component.scroll_up_button.color = color
    component.scroll_down_button.color = color
    component.scroll_up_button.pressed_color = pressed_color
    component.scroll_down_button.pressed_color = pressed_color


def add_scroll_encoder(component):
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(component, value, _):
        if value < 0:
            if component.can_scroll_up():
                component.scroll_up()
        elif component.can_scroll_down():
            component.scroll_down()

    component.add_control('scroll_encoder', scroll_encoder)