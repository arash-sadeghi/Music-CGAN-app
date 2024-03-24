import mido
import pretty_midi
import numpy as np
import pypianoroll
# from models.CONST_VARS import CONST
from CONST_VARS import CONST
import mido
import time
import pretty_midi
import rtmidi
import pypianoroll
# from mido import MidiFile, MidiPort
midi_filename = 'received_messages_pm.mid'
MIDI_INPUT_PORT = 'IAC Driver Bus 1'
TIME_WINDOW = 17 #! 10 is not enough
def listen4midi():
    '''
    listen to midi in port MIDI_INPUT_PORT for TIME_WINDOW seconds and then converts it to piano roll
    expected bass track
    '''

    pm_data = pretty_midi.PrettyMIDI()  # Create empty PrettyMIDI object
    bass = pretty_midi.Instrument(program=33) #! 33 is bass program code. got from CGAN repo

    midi_in = rtmidi.MidiIn()
    available_ports = midi_in.get_ports()
    if MIDI_INPUT_PORT not in available_ports:
        print(f"Virtual MIDI Port not found. Available ports: {available_ports}")
        return
    midi_in.open_port(available_ports.index(MIDI_INPUT_PORT))


    with mido.open_input() as port:
        start_time = time.time()
        end_time = start_time + TIME_WINDOW  # Listen for 10 seconds
        ons = {} #* this dictionary enables us to capture cords
        for message in port:
            print("message",message)
            if time.time() >= end_time:
                break
            # track.append(message)
            elif message.type == 'note_on':
                note_beg = time.time() - start_time
                ons[str(message.note)] = note_beg

            elif message.type == 'note_off':
                if str(message.note) in ons.keys():
                    note_end = time.time() - start_time
                    note = pretty_midi.Note(
                        velocity=message.velocity, #! this is not accurate becuse note on and note off velocities are different
                        pitch=message.note,
                        start=ons[str(message.note)],
                        end=note_end
                        )

                    bass.notes.append(note)  # Append note to first instrument

    pm_data.instruments.append(bass)
    # pm_data.write(midi_filename)
    # print(f"Received messages saved to '{midi_filename}'.")

    return midi_to_piano_roll(midi_data = pm_data)

def midi_to_piano_roll(midi_file_path = '',midi_data=None):

    if midi_data is None: 
        midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    multi_track = pypianoroll.from_pretty_midi(midi_data)
    multi_track.set_resolution(CONST.beat_resolution) 
    # multi_track.binarize()
    piano_roll = multi_track.stack()

    return piano_roll.squeeze() , multi_track.tempo

