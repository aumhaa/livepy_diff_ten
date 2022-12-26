from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface.components import find_nearest_color
from . import clamp, find_if, liveobj_valid
TRANSLATED_MIXER_PARAMETER_NAMES = {'Track Volume':'Volume', 
 'Track Panning':'Pan'}
UNDECLARED_QUANTIZED_PARAMETERS = {'AutoFilter':('LFO Sync Rate', ), 
 'AutoPan':('Sync Rate', ), 
 'BeatRepeat':('Gate', 'Grid', 'Interval', 'Offset', 'Variation'), 
 'Corpus':('LFO Sync Rate', ), 
 'Flanger':('Sync Rate', ), 
 'FrequencyShifter':('Sync Rate', ), 
 'GlueCompressor':('Ratio', 'Attack', 'Release'), 
 'MidiArpeggiator':('Offset', 'Synced Rate', 'Repeats', 'Ret. Interval', 'Transp. Steps'), 
 'MidiNoteLength':('Synced Length', ), 
 'MidiScale':('Base', ), 
 'MultiSampler':('L 1 Sync Rate', 'L 2 Sync Rate', 'L 3 Sync Rate'), 
 'Operator':('LFO Sync', ), 
 'OriginalSimpler':('L Sync Rate', ), 
 'Phaser':('LFO Sync Rate', )}
_current_song = None

def song(from_test=False, create_new=False, **k):
    global _current_song
    if from_test:
        k['create_new'] = create_new
    if not create_new:
        if liveobj_valid(_current_song):
            return _current_song
    _current_song = (Live.Application.get_application().get_document)(**k)
    return _current_song


def is_clip_or_slot(obj):
    return isinstance(obj, (Live.Clip.Clip, Live.ClipSlot.ClipSlot))


def is_scene(obj):
    return isinstance(obj, Live.Scene.Scene)


def is_drum_chain(obj):
    return isinstance(obj, Live.DrumChain.DrumChain)


def is_song_recording():
    return song().session_record or song().record_mode


def is_track_armed(track):
    return liveobj_valid(track) and track.can_be_armed and (track.arm or track.implicit_arm)


def any_track_armed():
    return any((t.can_be_armed and t.arm for t in song().tracks))


def scene_index(scene):
    return list(song().scenes).index(scene)


def scene_display_name(scene, strip_space=True):
    name = scene.name.strip() if strip_space else scene.name
    return name or 'Scene {}'.format(scene_index(scene) + 1)


def get_parameter_by_name(name, device):
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name == name and liveobj_valid(p) and p.is_enabled, device.parameters)


def parameter_display_name(parameter):
    if liveobj_valid(parameter):
        try:
            return parameter.display_name
        except AttributeError:
            return TRANSLATED_MIXER_PARAMETER_NAMES.get(parameter.name, parameter.name)

        return ''


def normalized_parameter_value(parameter):
    value = 0.0
    if liveobj_valid(parameter):
        param_range = parameter.max - parameter.min
        value = (parameter.value - parameter.min) / param_range
    return clamp(value, 0.0, 1.0)


def parameter_value_to_midi_value(parameter, max_value=128):
    return int(normalized_parameter_value(parameter) * (max_value - 1))


def is_parameter_quantized(parameter, device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(device, 'class_name', None)
        is_quantized = (parameter.is_quantized) or ((device_class in UNDECLARED_QUANTIZED_PARAMETERS) and (parameter.name in UNDECLARED_QUANTIZED_PARAMETERS[device_class]))
    return is_quantized


def toggle_or_cycle_parameter_value(parameter):
    if liveobj_valid(parameter):
        if parameter.is_quantized:
            if parameter.value + 1 > parameter.max:
                parameter.value = parameter.min
            else:
                parameter.value = parameter.value + 1
        else:
            parameter.value = parameter.max if parameter.value == parameter.min else parameter.min


def liveobj_color_to_midi_rgb_values(liveobj_predicate=None):

    def inner(obj):
        if liveobj_predicate is not None:
            if not liveobj_predicate(obj):
                return
            return (((obj.color & 16711680) >> 16) // 2,
             ((obj.color & 65280) >> 8) // 2,
             (obj.color & 255) // 2)

    return inner


def liveobj_color_to_value_from_palette(palette=None, fallback_table=None, liveobj_predicate=None):

    def inner(obj):
        if liveobj_predicate is not None:
            if not liveobj_predicate(obj):
                return
        try:
            return palette[obj.color]
        except (KeyError, IndexError):
            return find_nearest_color(fallback_table, obj.color)

    return inner