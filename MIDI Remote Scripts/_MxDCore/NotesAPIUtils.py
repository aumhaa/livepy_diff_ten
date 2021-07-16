from __future__ import absolute_import, print_function, unicode_literals
REQUIRED_MIDI_NOTE_ATTRS = ('pitch', 'start_time', 'duration')

def midi_note_to_dict(note):
    return {'note_id':note.note_id, 
     'pitch':note.pitch, 
     'start_time':note.start_time, 
     'duration':note.duration, 
     'velocity':note.velocity, 
     'mute':int(note.mute), 
     'probability':note.probability, 
     'velocity_deviation':note.velocity_deviation, 
     'release_velocity':note.release_velocity}


def midi_notes_to_notes_dict(notes):
    return {'notes': [midi_note_to_dict(note) for note in notes]}


def verify_note_specification_requirements(note_specification):
    missing_keys = set(REQUIRED_MIDI_NOTE_ATTRS) - set(note_specification.keys())
    if len(missing_keys) > 0:
        raise RuntimeError('Missing required keys: ', ', '.join(missing_keys))