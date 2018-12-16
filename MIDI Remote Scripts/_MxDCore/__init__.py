from __future__ import absolute_import, print_function, unicode_literals
from .MxDCore import MxDCore as _MxDCore
import sys, warnings

def set_manager(manager):
    assert manager != None
    assert _MxDCore.instance == None
    _MxDCore.instance = _MxDCore()
    _MxDCore.instance.set_manager(manager)


def disconnect():
    _MxDCore.instance.disconnect()
    del _MxDCore.instance


def execute_command(device_id, object_id, command, arguments):
    assert _MxDCore.instance != None
    assert isinstance(arguments, (str, unicode))
    if hasattr(_MxDCore.instance, command):
        try:
            with warnings.catch_warnings(record=True) as caught_warnings:
                _MxDCore.instance.update_device_context(device_id, object_id)
                function = getattr(_MxDCore.instance, command)
                function(device_id, object_id, arguments)
                for warning in caught_warnings:
                    _MxDCore.instance._warn(device_id, object_id, str(warning.message))

        except:
            if sys.exc_info()[0].__name__ == u'RuntimeError':
                assert_reason = str(sys.exc_info()[1])
            else:
                assert_reason = u'Invalid syntax'
            _MxDCore.instance._raise(device_id, object_id, assert_reason)

    else:
        _MxDCore.instance._raise(device_id, object_id, u'Unknown command: ' + command)
