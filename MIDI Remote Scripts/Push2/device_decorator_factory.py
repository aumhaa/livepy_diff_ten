from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from pushbase.decoration import DecoratorFactory
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .wavetable import InstrumentVectorDeviceDecorator

class DeviceDecoratorFactory(DecoratorFactory):
    DECORATOR_CLASSES = {u'OriginalSimpler': SimplerDeviceDecorator,
     u'Operator': OperatorDeviceDecorator,
     u'MultiSampler': SamplerDeviceDecorator,
     u'AutoFilter': AutoFilterDeviceDecorator,
     u'Eq8': Eq8DeviceDecorator,
     u'Compressor2': CompressorDeviceDecorator,
     u'Pedal': PedalDeviceDecorator,
     u'DrumBuss': DrumBussDeviceDecorator,
     u'Echo': EchoDeviceDecorator,
     u'InstrumentVector': InstrumentVectorDeviceDecorator,
     u'StereoGain': UtilityDeviceDecorator}

    @classmethod
    def generate_decorated_device(cls, device, additional_properties = {}, song = None, *a, **k):
        decorated = cls.DECORATOR_CLASSES[device.class_name](live_object=device, additional_properties=additional_properties, *a, **k)
        return decorated

    @classmethod
    def _should_be_decorated(cls, device):
        return liveobj_valid(device) and device.class_name in cls.DECORATOR_CLASSES

    def _get_decorated_object(self, device, additional_properties, song = None, *a, **k):
        return self.generate_decorated_device(device, additional_properties=additional_properties, *a, **k)
