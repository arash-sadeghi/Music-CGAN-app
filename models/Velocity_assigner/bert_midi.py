from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
from torch import nn
import torch.nn.functional as F
from transformers import BertConfig

print("[+] in bert_midi")

class BertMidi(nn.Module):
    PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
    MAX_INPUT_LENGTH = 510 #self.bert.config.max_position_embeddings

    def __init__(self, n_classes = 2):
        super().__init__()
        # self.bert = BertModel.from_pretrained(BertMidi.PRE_TRAINED_MODEL_NAME) #! this is the line that causes docker to not run
        self.bert = BertModel(config = BertConfig.from_json_file('models/Velocity_assigner/config.json')) 
        self.drop = nn.Dropout(p=0.3)
        self.l1 = nn.Linear(self.bert.config.hidden_size*BertMidi.MAX_INPUT_LENGTH , BertMidi.MAX_INPUT_LENGTH) 


    def forward(self, input_ids, attention_mask):
        bert_out = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        x = self.drop(bert_out.last_hidden_state)
        x = x.view(-1 , self.bert.config.hidden_size*BertMidi.MAX_INPUT_LENGTH)
        # res = [ F.sigmoid(self.l1[_](x[:,_])) for _ in range(MAX_INPUT_LENGTH)  ]
        res = self.l1(x)
        res = F.sigmoid(res)

        return res