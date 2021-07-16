from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .hybrid_reverb import HybridReverbDeviceDecorator
from .delay import DelayDeviceDecorator
from .chorus2 import Chorus2DeviceDecorator
from .corpus import CorpusDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .phasernew import PhaserNewDeviceDecorator
from .redux2 import Redux2DeviceDecorator
from .transmute import TransmuteDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .spectral import SpectralDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {'OriginalSimpler':SimplerDeviceDecorator, 
     'Operator':OperatorDeviceDecorator, 
     'MultiSampler':SamplerDeviceDecorator, 
     'AutoFilter':AutoFilterDeviceDecorator, 
     'Eq8':Eq8DeviceDecorator, 
     'Chorus2':Chorus2DeviceDecorator, 
     'Compressor2':CompressorDeviceDecorator, 
     'Corpus':CorpusDeviceDecorator, 
     'Pedal':PedalDeviceDecorator, 
     'PhaserNew':PhaserNewDeviceDecorator, 
     'DrumBuss':DrumBussDeviceDecorator, 
     'Echo':EchoDeviceDecorator, 
     'Hybrid':HybridReverbDeviceDecorator, 
     'InstrumentVector':WavetableDeviceDecorator, 
     'Spectral':SpectralDeviceDecorator, 
     'StereoGain':UtilityDeviceDecorator, 
     'Transmute':TransmuteDeviceDecorator, 
     'Delay':DelayDeviceDecorator, 
     'Redux2':Redux2DeviceDecorator}