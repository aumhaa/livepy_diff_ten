from __future__ import absolute_import, print_function, unicode_literals
from .launchkey_mini_mk3 import Launchkey_Mini_MK3
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[258], model_name=[u'Launchkey Mini MK3']),
     PORTS_KEY: [inport(props=[]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[SYNC]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return Launchkey_Mini_MK3(c_instance=c_instance)
