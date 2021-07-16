from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.base import const, nop
import ableton.v2.base.dependency as dependency

class Messenger(object):
    message = dependency(message=(const(nop)))