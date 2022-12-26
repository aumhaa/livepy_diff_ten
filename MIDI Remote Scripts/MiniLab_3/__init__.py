from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import is_clip_or_slot, is_drum_chain, liveobj_color_to_midi_rgb_values
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, SCRIPT, controller_id, inport, outport
from ableton.v3.control_surface.elements import create_rgb_color
from universal import UniversalControlSurface, UniversalControlSurfaceSpecification, create_skin
from .analog_lab import AnalogLabComponent
from .colors import Rgb, Skin
from .display import DisplayComponent
from .drum_group import DrumGroupComponent
from .elements import NUM_SCENES, NUM_TRACKS, Elements
from .mappings import create_mappings
from .midi import CONNECTION_MESSAGE, DISCONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE, SYSEX_START
from .transport import TransportComponent
rgb_function = liveobj_color_to_midi_rgb_values(liveobj_predicate=(lambda x: is_clip_or_slot(x) or is_drum_chain(x)))

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285,
                          product_ids=[8715],
                          model_name=['Minilab3']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[NOTES_CC])]}


def create_instance(c_instance):
    return MiniLab_3(Specification, c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    link_session_ring_to_track_selection = True
    link_session_ring_to_scene_selection = True
    num_tracks = NUM_TRACKS
    num_scenes = NUM_SCENES
    identity_response_id_bytes = (0, 32, 107)
    create_mappings_function = create_mappings
    hello_messages = (CONNECTION_MESSAGE, REQUEST_PROGRAM_MESSAGE)
    goodbye_messages = (DISCONNECTION_MESSAGE,)
    color_for_liveobj_function = lambda x: create_rgb_color(rgb_function(x))
    component_map = {'Drum_Group':DrumGroupComponent,  'Transport':TransportComponent}


class MiniLab_3(UniversalControlSurface):

    def setup(self):
        super().setup()
        AnalogLabComponent()
        display = DisplayComponent(self._identification, self.component_map['Transport'])
        display.shift_button.set_control_element(self.elements.shift_button)

    @staticmethod
    def _should_include_element_in_background(element):
        return 'Pad_Bank' not in element.name

    def _do_send_midi(self, midi_event_bytes):
        if midi_event_bytes[0] == SYSEX_START:
            super()._do_send_midi(midi_event_bytes)