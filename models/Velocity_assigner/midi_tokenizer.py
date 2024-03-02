import torch
from tqdm import tqdm
from miditok import REMI, TokenizerConfig  # here we choose to use REMI
from transformers import BertTokenizer
import json
import os 

class MidiBertTokenizer:
    PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
    def __init__(self) -> None:

        
        self.inp_tgt = {'input_ids':[], 'attention_mask':[],'input_tokens':[]}

        TOKENIZER_PARAMS = {
            "pitch_range": (21, 109),
            "beat_res": {(0, 4): 8, (4, 12): 4},
            "num_velocities": 32,
            "special_tokens": ["PAD", "BOS", "EOS", "MASK"],
            "use_chords": True,
            "use_rests": True,
            "use_tempos": True,
            "use_time_signatures": True,
            "use_programs": True,
            "num_tempos": 32,  # number of tempo bins
            "tempo_range": (40, 250),  # (min, max)
        }

        config_input = TokenizerConfig(**TOKENIZER_PARAMS)
        self.tokenizer_input = REMI(config_input)

        self.bert_tokenizer = BertTokenizer.from_pretrained(MidiBertTokenizer.PRE_TRAINED_MODEL_NAME)

    def tokenize_midi_file(self,file_path):
        try: #! some midi files are not structured well
            self.midi_tokens = self.tokenizer_input(file_path)  # automatically detects Score objects, paths, tokens
        except Exception as e:
            print(f"[-] Error reading {file_path}, Error: {e}")
            return
        
        token_length = len(self.midi_tokens.ids)
        
        input_midi_ids = []
        for i in range(token_length): #! hiding velocity information in target
            if 'Velocity' in self.midi_tokens.tokens[i]:
                input_midi_ids.append('[MASK]')
                velocity = int(self.midi_tokens.tokens[i].split('_')[1])
                assert velocity>0 #! just to make sure velocity 0 is not used as note off

                if velocity>=127:
                    print(velocity)

            else:
                input_midi_ids.append(str(self.midi_tokens.ids[i]))
            

        
        #! make input a single string
        input_str = ' '.join(_ for _ in input_midi_ids)

        inp_bert_token_ids = self.bert_tokenizer(input_str)
        inp_bert_tokens = self.bert_tokenizer.tokenize(input_str)


        #TODO: lenght might be smaller than 510
        for c in range(len(inp_bert_token_ids.input_ids)//510):
            self.inp_tgt['input_ids'].append(inp_bert_token_ids.input_ids[c*510:(c+1)*510])  #! 510 is bert capacity
            self.inp_tgt['attention_mask'].append(inp_bert_token_ids.attention_mask[c*510:(c+1)*510])  #! 510 is bert capacity
            self.inp_tgt['input_tokens'].append(inp_bert_tokens[c*510:(c+1)*510])  #! 510 is bert capacity


        remaining_tokens_num = len(inp_bert_tokens)%510
        pad_tokens_to_fill = 510 - remaining_tokens_num -2
        if remaining_tokens_num>0: #! some notes are remaning
            self.inp_tgt['input_ids'].append(inp_bert_token_ids.input_ids[(c+1)*510:]+[0]*pad_tokens_to_fill)  #! 510 is bert capacity
            self.inp_tgt['attention_mask'].append(inp_bert_token_ids.attention_mask[(c+1)*510:]+[1]*pad_tokens_to_fill)  #! 510 is bert capacity
            self.inp_tgt['input_tokens'].append(inp_bert_tokens[(c+1)*510:]+['[PAD]']*pad_tokens_to_fill)  #! 510 is bert capacity




