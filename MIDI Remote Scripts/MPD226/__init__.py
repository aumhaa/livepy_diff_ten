from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .MPD226 import MPD226

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2536, product_ids=[53], model_name=u'MPD226'),
     caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]), caps.outport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE])]}


def create_instance(c_instance):
    return MPD226(c_instance)
