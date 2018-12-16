from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {u'OriginalSimpler': SimplerDeviceDecorator,
     u'Operator': OperatorDeviceDecorator,
     u'MultiSampler': SamplerDeviceDecorator,
     u'AutoFilter': AutoFilterDeviceDecorator,
     u'Eq8': Eq8DeviceDecorator,
     u'Compressor2': CompressorDeviceDecorator,
     u'Pedal': PedalDeviceDecorator,
     u'DrumBuss': DrumBussDeviceDecorator,
     u'Echo': EchoDeviceDecorator,
     u'InstrumentVector': WavetableDeviceDecorator,
     u'StereoGain': UtilityDeviceDecorator}
