from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .fantom import FANTOM

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410,
                          product_ids=[544],
                          model_name=['FANTOM-6 7 8']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return FANTOM(c_instance=c_instance)