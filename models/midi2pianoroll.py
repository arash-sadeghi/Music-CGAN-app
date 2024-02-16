import mido
import pretty_midi
import numpy as np
import pypianoroll
from CONST_VARS import CONST
def midi_to_piano_roll(midi_file_path):

    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    multi_track = pypianoroll.from_pretty_midi(midi_data)
    multi_track.set_resolution(CONST.beat_resolution) 
    # multi_track.binarize()
    piano_roll = multi_track.stack()

    return piano_roll.squeeze() , multi_track.tempo

