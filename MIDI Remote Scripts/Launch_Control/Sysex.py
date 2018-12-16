from __future__ import absolute_import, print_function, unicode_literals
MODE_CHANGE_PREFIX = (240, 0, 32, 41, 2, 10, 119)
MIXER_MODE = (240, 0, 32, 41, 2, 10, 119, 8, 247)
SESSION_MODE = (240, 0, 32, 41, 2, 10, 119, 9, 247)
DEVICE_MODE = (240, 0, 32, 41, 2, 10, 119, 10, 247)

def make_automatic_flashing_message(channel):
    return (176 + channel, 0, 40)
