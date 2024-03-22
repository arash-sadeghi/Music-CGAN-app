import mido
import time
from random import randint
import time
import pretty_midi
file_name = __file__.split("/")[-1]
midi_file = "/Users/arashsadeghiamjadi/Desktop/Workdir/JamBuddy/Server_App/static/midi/1_funk_80_beat_4-4.mid"
class MIDI_imitator:
    MIDI_PORT = 'IAC Driver Bus 1'
    def __init__(self) -> None:
        pass

    def list_midi_output_ports(self):
        output_ports = mido.get_output_names()
        print("Available MIDI Output Ports:")
        for port in output_ports:
            print(port)


    def simulate_midi_messages(self):
        #!#################
        # midi_data = pretty_midi.PrettyMIDI("/Users/arashsadeghiamjadi/Desktop/Workdir/JamBuddy/Server_App/static/midi/out.midi")
        mid = mido.MidiFile(midi_file)

        # Iterate through the MIDI messages and print them
        # for i, msg in enumerate(mid):
        #     print(f"Message {i+1}: {msg}")
        #!#################


        # Open MIDI output port
        with mido.open_output(MIDI_imitator.MIDI_PORT) as out_port:
            print(f"Simulating MIDI messages on {MIDI_imitator.MIDI_PORT}. Press Ctrl+C to exit.")


            note =  60# randint(60, 72)  # Random note between C4 and C5
            velocity = 80#randint(40, 80) 
            try:
                # while True:
                for i, msg in enumerate(mid):
                    # Generate a random note-on message
                    note_time = time.time()
                    # msg = mido.Message('note_on', note=note, velocity=velocity)
                    # msg = mido.Message('note_on', note=note, velocity=velocity)

                    note += 1

                    # play_midi_message(convert_mido_to_pretty_midi(msg))

                    # Send the MIDI message
                    if "note" in msg.type or True:
                        out_port.send(msg)
                    

                        time.sleep(msg.time)  # Adjust the sleep time based on your preference

                    print(f"{[file_name]} message {msg}")

            except KeyboardInterrupt:
                print("\nExiting...")

if __name__ == '__main__':
    emit = MIDI_imitator()
    emit.list_midi_output_ports()
    emit.simulate_midi_messages()