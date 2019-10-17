from __future__ import absolute_import, print_function, unicode_literals
from .launchpad_x import Launchpad_X
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[259], model_name=[u'Launchpad MK3']),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC,
                  SYNC,
                  SCRIPT,
                  REMOTE])]}


def create_instance(c_instance):
    return Launchpad_X(c_instance=c_instance)
