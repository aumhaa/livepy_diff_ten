from __future__ import absolute_import, print_function, unicode_literals
from .RemoteSL import RemoteSL

def create_instance(c_instance):
    return RemoteSL(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[3], model_name=u'ReMOTE ZeRO SL'),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, REMOTE, SCRIPT]),
                 inport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SYNC]),
                 outport(props=[SCRIPT]),
                 outport(props=[])]}
