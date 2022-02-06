from __future__ import absolute_import, print_function, unicode_literals
from . import liveobj_valid

def is_song_recording(song):
    return song.session_record or song.record_mode


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


def toggle_or_cycle_parameter_value(parameter):
    if liveobj_valid(parameter):
        if parameter.is_quantized:
            if parameter.value + 1 > parameter.max:
                parameter.value = parameter.min
            else:
                parameter.value = parameter.value + 1
        else:
            parameter.value = parameter.max if parameter.value == parameter.min else parameter.min