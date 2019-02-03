from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, imap
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        return chain(*imap(lambda x: self._translate_string(unicode(x).strip()), display._logical_segments))
