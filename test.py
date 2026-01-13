import outlines
from transformers import AutoTokenizer, AutoModelForCausalLM, BertTokenizer, BertForSequenceClassification
from typing import Literal
from pydantic import BaseModel, Json, ValidationError
from enum import Enum
from huggingface_hub import login
import torch
import string
from bs4 import BeautifulSoup
import requests
import numpy as np

from UrlObject import UrlObject
from UrlEnum import UrlEnum
from getWebpageText import getWebpageText

url = 'https://www.cnn.com/2025/12/10/style/notre-dame-claire-tabouret-stained-glass-windows'
webpageText = getWebpageText(UrlObject(url, UrlEnum.CNN))

### Get Summary and Title ###
# Load tokenizer and model
model_id = "microsoft/bitnet-b1.58-2B-4T"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map=device,
    dtype=torch.bfloat16,
    local_files_only=False
)

context = "You are an AI assistant."
userPrompt = "Summarize: "

# Apply the chat template
messages = [
    {"role": "assistant", "content": context},
    {"role": "user", "content": userPrompt + webpageText}
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)

# Generate response
chat_outputs = model.generate(**chat_input, max_new_tokens=500)
summaryOfText = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True) # Decode only the response part


userPrompt = "Summarize in 5 words: "
# Apply the chat template
messages = [
    {"role": "assistant", "content": context},
    {"role": "user", "content": userPrompt + summaryOfText.replace('**', '').replace('\n', " ")}
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)

# Generate response
chat_outputs = model.generate(**chat_input, max_new_tokens=50)
oneSentenceSummary = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True) # Decode only the response part

nextSentenceIdx = oneSentenceSummary.find('\n')
if(nextSentenceIdx > 0):
    print("One Sentence Summary:\n", oneSentenceSummary[0:nextSentenceIdx])
else:
    print("One Sentence Summary:\n", oneSentenceSummary)

lastDotIdx = summaryOfText.rfind('.')
if(lastDotIdx > 0):
    print('Summary:\n', summaryOfText[0:lastDotIdx+1])
else:
    print('Summary:\n', summaryOfText)

del model, tokenizer

model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(model_id,
                                         device_map=device,
                                         dtype=torch.bfloat16,
                                         local_files_only=False),
    AutoTokenizer.from_pretrained(model_id)
)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained ("cssupport/bert-news-class").to(device)

def predict(text, model, tokenizer, maxLengthOfText = 8000):
    id_to_class = {0: 'Arts', 1: 'Arts & Culture', 2: 'Black Voices', 3: 'Business', 4: 'College', 5: 'Comedy', 6: 'Crime', 7: 'Culture & Arts', 8: 'Education', 9: 'Entertainment', 10: 'Environment', 11: 'Fifty', 12: 'Food & Drink', 13: 'Good News', 14: 'Green', 15: 'Health', 16: 'Home & Living', 17: 'Impact', 18: 'Latino Voices', 19: 'Media', 20: 'Money', 21: 'Parenting', 22: 'Parents', 23: 'Politics', 24: 'Queer Voices', 25: 'Religion', 26: 'Science', 27: 'Sports', 28: 'Style', 29: 'Style & Beauty', 30: 'Taste', 31: 'Tech', 32: 'The Worldpost', 33: 'Travel', 34: 'U.S. News', 35: 'Weddings', 36: 'Weird News', 37: 'Wellness', 38: 'Women', 39: 'World News', 40: 'Worldpost'}
    
    if(len(text)>maxLengthOfText):
        text = text.replace('**', '').replace('\n', " ")[0:maxLengthOfText].rfind('.')
    
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt').to(device)
    with torch.no_grad():
        logits = model(inputs['input_ids'], inputs['attention_mask'])[0]
    # Get the predicted class index
    pred_class_idx = torch.argmax(logits, dim=1).item()
    return id_to_class[pred_class_idx]

print("Topic:", predict(summaryOfText, model, tokenizer))

print("I am a Small Language Model (SLM) generating a summary based on the first 8000 characters I see. Take what I say with a grain of salt. Thanks.")
print("Link to original article:", url)