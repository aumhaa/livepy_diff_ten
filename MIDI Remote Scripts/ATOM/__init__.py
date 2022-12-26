from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import is_clip_or_slot, is_scene, liveobj_valid
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import ArmedTargetTrackComponent, TranslatingBackgroundComponent
from universal import UniversalControlSurface, UniversalControlSurfaceSpecification, create_skin
from . import midi
from .colors import LIVE_COLOR_INDEX_TO_RGB, Rgb
from .drum_group import DrumGroupComponent
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .keyboard import KeyboardComponent
from .mappings import create_mappings
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[518],
                          model_name=['ATOM']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return ATOM(c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    target_track_component_type = ArmedTargetTrackComponent
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    identity_request = midi.NATIVE_MODE_ON_MESSAGE
    custom_identity_response = (191, 127, 127)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    color_for_liveobj_function = --- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              is_clip_or_slot
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_GLOBAL              is_scene
               10  LOAD_FAST                'obj'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  POP_JUMP_IF_FALSE    30  'to 30'
             16_0  COME_FROM             6  '6'
               16  LOAD_GLOBAL              LIVE_COLOR_INDEX_TO_RGB
               18  LOAD_METHOD              get
               20  LOAD_FAST                'obj'
               22  LOAD_ATTR                color_index
               24  LOAD_CONST               0
               26  CALL_METHOD_2         2  '2 positional arguments'
               28  RETURN_VALUE_LAMBDA
             30_0  COME_FROM            14  '14'

 L.  68        30  LOAD_CONST               None
               32  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    component_map = {'Drum_Group':partial(DrumGroupComponent, translation_channel=midi.DRUM_CHANNEL), 
     'Keyboard':partial(KeyboardComponent, midi.KEYBOARD_CHANNEL), 
     'Translating_Background':partial(TranslatingBackgroundComponent,
       translation_channel=midi.USER_CHANNEL)}


class ATOM(UniversalControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super().port_settings_changed()

    def drum_group_changed(self, drum_group):
        self.component_map['Note_Modes'].selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'