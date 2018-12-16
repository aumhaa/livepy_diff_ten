from __future__ import absolute_import, print_function, unicode_literals
from .MaxForLive import MaxForLive
from ableton.v2.control_surface.capabilities import GENERIC_SCRIPT_KEY

def get_capabilities():
    return {GENERIC_SCRIPT_KEY: True}


def create_instance(c_instance):
    return MaxForLive(c_instance=c_instance)
