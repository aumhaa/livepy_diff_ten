from __future__ import absolute_import, print_function, unicode_literals
from .AxiomPro import AxiomPro

def create_instance(c_instance):
    return AxiomPro(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8227], model_name=u'Axiom Pro 49'),
     PORTS_KEY: [inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}
