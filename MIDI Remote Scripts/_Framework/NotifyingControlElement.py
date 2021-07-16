from __future__ import absolute_import, print_function, unicode_literals
from .SubjectSlot import Subject, SubjectEvent
from .ControlElement import ControlElement

class NotifyingControlElement(Subject, ControlElement):
    __subject_events__ = (
     SubjectEvent(name='value',
       doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)