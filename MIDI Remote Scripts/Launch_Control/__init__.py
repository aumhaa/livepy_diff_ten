from __future__ import absolute_import, print_function, unicode_literals
from .LaunchControl import LaunchControl
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[52], model_name=u'Launch Control'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), outport(props=[NOTES_CC, SCRIPT])]}


def create_instance(c_instance):
    return LaunchControl(c_instance)
