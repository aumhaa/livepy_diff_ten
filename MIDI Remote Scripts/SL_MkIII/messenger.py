from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, nop
from ableton.v2.base.dependency import dependency

class Messenger(object):
    message = dependency(message=const(nop))
