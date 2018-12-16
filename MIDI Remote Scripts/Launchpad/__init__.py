from __future__ import absolute_import, print_function, unicode_literals
from .Launchpad import Launchpad

def create_instance(c_instance):
    u""" Creates and returns the Launchpad script """
    return Launchpad(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[14], model_name=u'Launchpad'),
     PORTS_KEY: [inport(props=[NOTES_CC, REMOTE, SCRIPT]), outport(props=[NOTES_CC, REMOTE, SCRIPT])]}
