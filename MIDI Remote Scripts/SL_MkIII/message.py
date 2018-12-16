from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import TextDisplayControl
NUM_MESSAGE_SEGMENTS = 2

class MessageComponent(Component):
    display = TextDisplayControl(segments=(u'',) * NUM_MESSAGE_SEGMENTS)

    def __call__(self, *messages):
        for index, message in izip(xrange(NUM_MESSAGE_SEGMENTS), messages):
            self.display[index] = message if message else u''
