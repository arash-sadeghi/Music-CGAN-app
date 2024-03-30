import pretty_midi
import pypianoroll
# from models.CONST_VARS import CONST
from CONST_VARS import CONST

def midi_to_piano_roll(midi_file_path = '',midi_data=None):

    if midi_data is None: 
        midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    else:
        midi_data.time_signature_changes.append(pretty_midi.TimeSignature(numerator=4,denominator=4,time=0))
    multi_track = pypianoroll.from_pretty_midi(midi_data,algorithm='strict')
    multi_track.set_resolution(CONST.beat_resolution) 
    multi_track.binarize()
    piano_roll = multi_track.stack()
    multi_track.write("static/midi/debug/debug_from_midi_to_piano_roll.midi")
    return piano_roll.squeeze() , multi_track.tempo

