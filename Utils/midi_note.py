
import pretty_midi
import numpy as np

def midi_note(notesClass,block_time):
    pitch=0
    for note in notesClass:
        if note.start<=block_time and note.end>=block_time:
            pitch=note.pitch
            break

    return pitch