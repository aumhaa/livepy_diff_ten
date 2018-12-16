from __future__ import absolute_import, print_function, unicode_literals
from .Axiom import Axiom

def create_instance(c_instance):
    return Axiom(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[408], model_name=u'USB Axiom 25'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[PLAIN_OLD_MIDI]), outport(props=[SCRIPT])]}
