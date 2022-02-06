from __future__ import absolute_import, print_function, unicode_literals
from abc import ABC, abstractmethod
from collections import namedtuple
from ...base import old_hasattr

class Color(ABC):

    @abstractmethod
    def draw(self, interface):
        pass


class SimpleColor(Color):

    def __init__(self, value, channel=None, *a, **k):
        (super().__init__)(*a, **k)
        self._value = value
        self._channel = channel

    @property
    def midi_value(self):
        return self._value

    def draw(self, interface):
        interface.send_value((self._value), channel=(self._channel))


ColorPart = namedtuple('ColorPart', 'value channel', defaults=(0, None))

class ComplexColor(Color):

    def __init__(self, color_parts, *a, **k):
        (super().__init__)(*a, **k)
        self._color_parts = color_parts

    @property
    def midi_value(self):
        return self._color_parts[0].value

    def draw(self, interface):
        for part in self._color_parts:
            interface.send_value((part.value), channel=(part.channel))


class FallbackColor(Color):

    def __init__(self, rgb_color, fallback_color):
        self._rgb_color = rgb_color
        self._fallback_color = fallback_color

    @property
    def midi_value(self):
        return self._rgb_color.midi_value

    def draw(self, interface):
        if old_hasattr(interface, 'is_rgb') and interface.is_rgb:
            self._rgb_color.draw(interface)
        else:
            self._fallback_color.draw(interface)