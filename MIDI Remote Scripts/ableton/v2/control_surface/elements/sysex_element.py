from __future__ import absolute_import, print_function, unicode_literals
from ..input_control_element import InputControlElement, MIDI_SYSEX_TYPE
from .. import midi

class SysexElement(InputControlElement):
    u"""
    Control element for sending and receiving sysex message.
    
    Set sysex_identifier to the unique static part of the sysex message, to notify
    the value event about incoming sysex messages.
    
    send_message_generator should be a function object that takes the arguments of
    send_value and generates a valid sysex message. send_value will raise an error
    if the generated message is not valid.
    
    enquire_message is the sysex message for requesting a value. Use enquire_value to
    send out the message.
    
    default_value is being used when calling reset on the element. The value is passed
    as an argument to send_value. Setting the property to None will disable sending
    a value when resetting the element (default).
    """

    def __init__(self, send_message_generator = None, enquire_message = None, default_value = None, *a, **k):
        super(SysexElement, self).__init__(msg_type=MIDI_SYSEX_TYPE, *a, **k)
        self._send_message_generator = send_message_generator
        self._enquire_message = enquire_message
        self._default_value = default_value

    def send_value(self, *arguments):
        assert self._send_message_generator is not None
        message = self._send_message_generator(*arguments)
        assert midi.is_valid_sysex(message), u'Trying to send sysex message %r, which is not valid.' % map(hex, message)
        self._do_send_value(message)

    def enquire_value(self):
        assert self._enquire_message is not None
        self.send_midi(self._enquire_message)

    def reset(self):
        if self._default_value is not None:
            self.send_value(self._default_value)

    def _do_send_value(self, message):
        self.send_midi(message)
