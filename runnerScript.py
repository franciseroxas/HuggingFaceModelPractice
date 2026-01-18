#For ML models
import outlines
from transformers import AutoTokenizer, AutoModelForCausalLM, BertTokenizer, BertForSequenceClassification
import torch

#For type casting
from typing import Literal
from pydantic import BaseModel, Json, ValidationError
from enum import Enum
import string
import numpy as np
import csv
import pandas as pd
import time

#For data scraping
from bs4 import BeautifulSoup
import requests

#My own functions to organize the data
from UrlObject import UrlObject
from UrlEnum import UrlEnum
from getWebpageText import getWebpageText
from getArticleLinksFromUrlHomepage import getArticleLinksFromUrlHomepage
from getWebpageTitle import getWebpageTitle

#Function call to run the entire pipeline. This name will be replaced in the future. 
def runnerScript():
    #Get a persistent requests session
    headers = {
        'user-agent': 'My app',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',}
        
    #Request object
    requestSession = requests.session()
    
    #Get a list of all article links on the url home page
    links = getArticleLinksFromUrlHomepage(url = 'https://apnews.com/', requestSession = requestSession, headers = headers)
    
    #Define variables to be used for summarization 
    sml_summarizer_model_id = "microsoft/bitnet-b1.58-2B-4T"
    bert_model_id = 'bert-base-uncased'
    bert_finetuned_model_id = "cssupport/bert-news-class"
                                    
    #Create variables to hold the article outputs
    listOfArticleTitles = []
    listOfArticleShortSummarys = []
    listOfArticleLargeSummarys = []
    listOfArticleTopics = []
    listOfArticleUrls = []
    
    #Get a device to run the models on 
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    # Load tokenizer and model
    slm_tokenizer = AutoTokenizer.from_pretrained(sml_summarizer_model_id)
    slm_model = AutoModelForCausalLM.from_pretrained(
        sml_summarizer_model_id,
        device_map=device,
        dtype=torch.bfloat16,
        local_files_only=False
    )
    
    #Load the bert toknizer
    bert_tokenizer = BertTokenizer.from_pretrained(bert_model_id)
    
    #Load the fine-tuned bert model for new articles
    bert_model = BertForSequenceClassification.from_pretrained(bert_finetuned_model_id).to(device)
    
    #Wait a little time before accessing the next article
    time.sleep(1)
        
    for i in range(10):#len(links)):):
        ### Get the text from the article url ###
        url = links[i]
        
        articleTitle = getWebpageTitle(UrlObject(url, UrlEnum.AP_NEWS), requestSession = requestSession, headers = headers)
        webpageText = getWebpageText(UrlObject(url, UrlEnum.AP_NEWS), requestSession = requestSession, headers = headers)
        
        print("Title of Article:", articleTitle)

        #############################
        ### Get Summary and Title ###
        #############################        

        context = "You are an AI assistant."
        userPrompt = "Summarize: "

        # Apply the chat template
        messages = [
            {"role": "assistant", "content": context},
            {"role": "user", "content": userPrompt + webpageText}
        ]
        prompt = slm_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        chat_input = slm_tokenizer(prompt, return_tensors="pt").to(slm_model.device)

        # Generate response
        chat_outputs = slm_model.generate(**chat_input, max_new_tokens=800)
        summaryOfText = slm_tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True) # Decode only the response part

        ##########################################
        ### Get the short one sentence summary ###
        ##########################################

        userPrompt = "Summarize in a single sentence: "
        # Apply the chat template
        messages = [
            {"role": "assistant", "content": context},
            {"role": "user", "content": userPrompt + webpageText}
        ]
        prompt = slm_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        chat_input = slm_tokenizer(prompt, return_tensors="pt").to(slm_model.device)

        # Generate response
        chat_outputs = slm_model.generate(**chat_input, max_new_tokens=50)
        oneSentenceSummary = slm_tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True) # Decode only the response part

        #Print the one sentence summary
        nextSentenceIdx = oneSentenceSummary.find('\n')
        if(nextSentenceIdx > 0):
            oneSentenceSummary = oneSentenceSummary[0:nextSentenceIdx]
            
        print("One Sentence Summary:\n", oneSentenceSummary)

        #Print the full summary        
        print('Summary:\n', summaryOfText)

        ####################################
        ### Get the topic of the article ###
        ####################################
        
        try:
            #Get the topic of the text
            topicOfText = predictTopicOfArticle(summaryOfText, bert_model, bert_tokenizer, device = device)
        except Exception as e:
            topicOfText = "Error when getting topic."
            print(repr(e))

        print("Topic:", topicOfText)

        ########################
        ### Print disclaimer ###
        ########################

        print("I am a Small Language Model (SLM) generating a summary based on the first 10000 characters I see. Take what I say with a grain of salt. Thanks.")
        print("Link to original article:", url)
        
        listOfArticleTitles.append(articleTitle)
        listOfArticleShortSummarys.append(summaryToAllowableCsvText(oneSentenceSummary))
        listOfArticleLargeSummarys.append(summaryToAllowableCsvText(summaryOfText))
        listOfArticleTopics.append(topicOfText)
        listOfArticleUrls.append(url)
        
        #Wait a little time before accessing the next article
        time.sleep(1)
    
    #Create a data frame and write to a csv
    df = pd.DataFrame({"Article Title":        listOfArticleTitles,
                       "One_Sentence_Summary": listOfArticleShortSummarys,
                       "Full_Summary":         listOfArticleLargeSummarys,
                       "Topic":                listOfArticleTopics,
                       "URL":                  listOfArticleUrls})
    df.to_csv('output.csv', sep = ',') 
    return df

### Helper functions 
def predictTopicOfArticle(text, model, tokenizer, maxLengthOfText = 5000, device = 'cpu'):
    id_to_class = {0: 'Arts', 1: 'Arts & Culture', 
                   2: 'Black Voices', 3: 'Business', 
                   4: 'College', 5: 'Comedy', 
                   6: 'Crime', 7: 'Culture & Arts', 
                   8: 'Education', 9: 'Entertainment', 
                   10: 'Environment', 11: 'Fifty', 
                   12: 'Food & Drink', 13: 'Good News', 
                   14: 'Green', 15: 'Health', 
                   16: 'Home & Living', 17: 'Impact', 
                   18: 'Latino Voices', 19: 'Media', 
                   20: 'Money', 21: 'Parenting', 
                   22: 'Parents', 23: 'Politics', 
                   24: 'Queer Voices', 25: 'Religion', 
                   26: 'Science', 27: 'Sports', 
                   28: 'Style', 29: 'Style & Beauty', 
                   30: 'Taste', 31: 'Tech', 
                   32: 'The Worldpost', 33: 'Travel', 
                   34: 'U.S. News', 35: 'Weddings', 
                   36: 'Weird News', 37: 'Wellness', 
                   38: 'Women', 39: 'World News', 
                   40: 'Worldpost'}
    
    #Truncate the text if it is too large
    if(len(text)>maxLengthOfText):
        text = text[0:maxLengthOfText]

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt').to(device)
    with torch.no_grad():
        logits = model(inputs['input_ids'], inputs['attention_mask'])[0]
        
    # Get the predicted class index
    pred_class_idx = torch.argmax(logits, dim=1).item()
    return id_to_class[pred_class_idx]
    
#Replace commas and new lines so that the summaries can be added to a csv file
def summaryToAllowableCsvText(summary):
    summary = summary.replace(',', '[COMMA]')
    summary = summary.replace('\n', '[NEW_LINE]')
    return summary
    
if __name__ == "__main__":
    runnerScript()