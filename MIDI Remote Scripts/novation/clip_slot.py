from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, depends
import ableton.v2.control_surface.components as ClipSlotComponentBase

class FixedLengthClipSlotComponent(ClipSlotComponentBase):

    @depends(fixed_length_recording=(const(None)))
    def __init__(self, fixed_length_recording, *a, **k):
        (super(FixedLengthClipSlotComponent, self).__init__)(*a, **k)
        self._fixed_length_recording = fixed_length_recording

    def _do_launch_clip(self, fire_state):
        slot = self._clip_slot
        if self._fixed_length_recording.should_start_recording_in_slot(slot):
            self._fixed_length_recording.start_recording_in_slot(slot)
        else:
            super(FixedLengthClipSlotComponent, self)._do_launch_clip(fire_state)