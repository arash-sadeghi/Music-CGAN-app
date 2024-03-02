from bert_midi import BertMidi
from  midi_tokenizer import MidiBertTokenizer
import torch

class VelocityAssigner:
    WEIGHTS_URL = ''
    SCALE_FACTOR = 127 #TODO model is not trained on this. Models scale factor is 200
    def __init__(self):
        self.bert = BertMidi()
        self.midi_tokenizer = MidiBertTokenizer()
        print('[+] loading weights')
        
        w = torch.load('models/Velocity_assigner/weights_1500.pts',map_location=torch.device('cpu')) 
        self.bert.load_state_dict(w)


    def assing_velocity2midi(self,midi_file_path):
        self.midi_tokenizer.tokenize_midi_file(midi_file_path)
        input_ids_torch = torch.tensor(self.midi_tokenizer.inp_tgt['input_ids']) 
        bert_velocities = self.bert.forward(
            input_ids_torch ,
            torch.tensor(self.midi_tokenizer.inp_tgt['attention_mask']))
        
        self.bert_out2midi(bert_velocities ,self.midi_tokenizer.inp_tgt['input_tokens'] ,input_ids_torch )
  
    def bert_out2midi(self,bert_out,input_tokens ,input_ids_torch):
        bert_out_masked = (input_ids_torch == 103)*bert_out

        bert_out_masked = bert_out_masked.view(1,bert_out_masked.shape[0]*bert_out_masked.shape[1]).squeeze()

        velocities = bert_out_masked[bert_out_masked != 0]*VelocityAssigner.SCALE_FACTOR


        vel_indx = 0
        for counter , token in enumerate(self.midi_tokenizer.midi_tokens.tokens):
            if 'Velocity' in token:
                self.midi_tokenizer.midi_tokens.tokens[counter] = 'Velocity_'+str(int(velocities[vel_indx]))
                vel_indx += 1
                

        music = self.midi_tokenizer.tokenizer_input(self.midi_tokenizer.midi_tokens.tokens)



if __name__ == '__main__':
    va = VelocityAssigner()
    va.assing_velocity2midi('static/midi/1_funk_80_beat_4-4.mid')