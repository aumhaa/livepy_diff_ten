from __future__ import absolute_import, print_function, unicode_literals
import Live

def is_set_to_split_stereo(mixer):
    modes = Live.MixerDevice.MixerDevice.panning_modes
    return modes.stereo_split == getattr(mixer, u'panning_mode', modes.stereo)


def has_pan_mode(mixer):
    return hasattr(mixer, u'panning_mode')
