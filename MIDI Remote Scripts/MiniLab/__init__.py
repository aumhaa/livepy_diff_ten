from __future__ import absolute_import, print_function, unicode_literals
from .MiniLab import MiniLab
import _Framework.Capabilities as caps

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=7285, product_ids=[516], model_name=[u'Arturia MINILAB']),
     caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]), caps.outport(props=[caps.SCRIPT])]}


def create_instance(c_instance):
    return MiniLab(c_instance)
