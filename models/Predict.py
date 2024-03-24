# from models.Generator import Generator
# from models.midi2pianoroll import midi_to_piano_roll , listen4midi
# from models.CONST_VARS import CONST

from Generator import Generator
from midi2pianoroll import midi_to_piano_roll , listen4midi
from CONST_VARS import CONST


import torch
import numpy as np 
import os 
from pypianoroll import Multitrack, Track
import pypianoroll 

class Predictor:
    def __init__(self) -> None:
        self.generator = Generator()
        self.generator.load_state_dict(torch.load('models/training_output_path_rootgenerator_20000.pth'))
        self.generator.eval() #! this solve error thrown by data length
    
    def generate_drum(self,bass_url = ''):
        # bass_piano_roll , tempo_array = midi_to_piano_roll(bass_url)
        bass_piano_roll , tempo_array = listen4midi()
        bass_piano_roll = torch.tensor(bass_piano_roll)
        bass_piano_roll = bass_piano_roll[:,CONST.lowest_pitch:CONST.lowest_pitch + CONST.n_pitches] #! not sure if this corresponds to same range as generator pitch
        bass_piano_roll = bass_piano_roll[0:bass_piano_roll.shape[0]//64*64,:].view(-1,64,72)

        latent = torch.randn(bass_piano_roll.shape[0], CONST.latent_dim)
        
        latent = latent.type(torch.float32)
        bass_piano_roll = bass_piano_roll.type(torch.float32)

        res = self.generator(latent,bass_piano_roll)

        #* reshaping data inorder to be saved as image
        temp = torch.cat((res.cpu().detach(),bass_piano_roll.unsqueeze(1)),axis = 1).numpy()
        temp = temp.transpose(1,0,2,3)
        # temp = res.detach().numpy().transpose(1,0,2,3)
        temp = temp.reshape(temp.shape[0] , temp.shape[1] * temp.shape[2] , temp.shape[3])

        tracks = []
        # for idx, (program, is_drum, track_name) in enumerate(zip([0], [True], ['Drum'])):

        for idx, (program, is_drum, track_name) in enumerate(zip([0,33], [True,False], ['Drum','Bass'])):
            # pianoroll = np.pad(np.concatenate(data[:4], 1)[idx], ((0, 0), (lowest_pitch, 128 - lowest_pitch - n_pitches)))
            pianoroll = np.pad(temp[idx] > 0.5,((0, 0), (CONST.lowest_pitch, 128 - CONST.lowest_pitch - CONST.n_pitches)))
            tracks.append(Track(name=track_name,program=program,is_drum=is_drum,pianoroll=pianoroll))

        m = Multitrack(tracks=tracks,tempo=tempo_array,resolution=CONST.beat_resolution)
        #! save music to npz -> midi
        m.save('static/generated_drum.npz')
        tmp = pypianoroll.load('static/generated_drum.npz')
        tmp.write('static/generated_drum.midi')

        return 'static/generated_drum.midi'

if __name__ == '__main__':
    p = Predictor()
    t1 = p.generate_drum()
