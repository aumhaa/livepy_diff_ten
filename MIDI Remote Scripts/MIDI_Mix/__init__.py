from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .MIDI_Mix import MIDI_Mix

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2536, product_ids=[49], model_name=u'MIDI Mix'),
     caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT]), caps.outport(props=[caps.NOTES_CC, caps.SCRIPT])]}


def create_instance(c_instance):
    return MIDI_Mix(c_instance)
