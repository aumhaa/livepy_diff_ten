from __future__ import absolute_import, print_function, unicode_literals
import _Framework.TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._punch_in_toggle.is_momentary = False
        self._punch_out_toggle.is_momentary = False