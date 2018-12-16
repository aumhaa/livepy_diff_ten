from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import BooleanContext, const, has_event, listens
from ..input_control_element import InputControlElement, MIDI_CC_TYPE
from ..skin import Skin

class ButtonValue(object):
    u"""
    Basic type for button values, so global constants are symbolically
    different from integers.
    """
    midi_value = 0

    def __init__(self, midi_value = None, *a, **k):
        super(ButtonValue, self).__init__(*a, **k)
        if midi_value is not None:
            self.midi_value = midi_value

    def __int__(self):
        return self.midi_value

    def __eq__(self, other):
        try:
            return id(self) == id(other) or self.midi_value == other
        except NotImplementedError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self != OFF_VALUE


ON_VALUE = ButtonValue(127)
OFF_VALUE = ButtonValue(0)

class DummyUndoStepHandler(object):

    def begin_undo_step(self):
        pass

    def end_undo_step(self):
        pass


class ButtonElementMixin(object):
    u"""
    Mixin for sending values to button-like control-elements elements.
    """

    def set_light(self, is_turned_on):
        if is_turned_on:
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        self.send_value(ON_VALUE)

    def turn_off(self):
        self.send_value(OFF_VALUE)


class ButtonElement(InputControlElement, ButtonElementMixin):
    u"""
    Class representing a button a the controller
    """

    class ProxiedInterface(InputControlElement.ProxiedInterface, ButtonElementMixin):
        is_momentary = const(True)
        is_pressed = const(False)

    def __init__(self, is_momentary, msg_type, channel, identifier, skin = Skin(), undo_step_handler = DummyUndoStepHandler(), *a, **k):
        super(ButtonElement, self).__init__(msg_type, channel, identifier, *a, **k)
        self.__is_momentary = bool(is_momentary)
        self._last_received_value = -1
        self._undo_step_handler = undo_step_handler
        self._skin = skin
        self._drawing_via_skin = BooleanContext()

    def is_momentary(self):
        u""" returns true if the buttons sends a message on being released """
        return self.__is_momentary

    def message_map_mode(self):
        assert self.message_type() is MIDI_CC_TYPE
        return Live.MidiMap.MapMode.absolute

    def is_pressed(self):
        return self.__is_momentary and int(self._last_received_value) > 0

    def set_light(self, value):
        if hasattr(value, u'draw'):
            value.draw(self)
        elif isinstance(value, bool):
            super(ButtonElement, self).set_light(value)
        else:
            self._set_skin_light(value)

    def _set_skin_light(self, value):
        color = None
        try:
            color = self._skin[value]
            self._do_draw(color)
        finally:
            if has_event(color, u'midi_value'):
                self.__on_midi_value_changed.subject = color
            else:
                self._disconnect_color_listener()

    def _do_draw(self, color):
        with self._drawing_via_skin():
            color.draw(self)

    @listens(u'midi_value')
    def __on_midi_value_changed(self, *a):
        self._do_draw(self.__on_midi_value_changed.subject)

    def send_value(self, value, force = False, channel = None):
        if not self._drawing_via_skin:
            self._disconnect_color_listener()
        super(ButtonElement, self).send_value(value, force, channel)

    def receive_value(self, value):
        pressed_before = self.is_pressed()
        self._last_received_value = value
        if not pressed_before and self.is_pressed():
            self._undo_step_handler.begin_undo_step()
        super(ButtonElement, self).receive_value(value)
        if pressed_before and not self.is_pressed():
            self._undo_step_handler.end_undo_step()

    def disconnect(self):
        super(ButtonElement, self).disconnect()
        self._undo_step_handler = None

    def _disconnect_color_listener(self):
        self.__on_midi_value_changed.subject = None
