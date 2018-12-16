from __future__ import absolute_import, print_function, unicode_literals
from .komplete_kontrol_a import KompleteKontrolA

def create_instance(c_instance):
    return KompleteKontrolA(c_instance=c_instance)
