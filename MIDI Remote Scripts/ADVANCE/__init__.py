from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .Advance import Advance

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2536, product_ids=[46, 47, 48], model_name=[u'ADVANCE25', u'ADVANCE49', u'ADVANCE61']),
     caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]), caps.outport(props=[caps.NOTES_CC, caps.SCRIPT])]}


def create_instance(c_instance):
    return Advance(c_instance)
