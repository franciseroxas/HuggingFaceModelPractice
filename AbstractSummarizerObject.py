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

#Abstract Wrapper object for calling models from hugging face. Includes a "bad" summarizer that just limits the text to a certain number of characters to speed up unit testing of the pipeline.
class AbstractSummarizerObject:
    oneSentenceSummary_:str #AI generated "headline of the text"
    summaryOfText_:str #Summary of text
    topic_:str #AI predicted topic
    summarizerModel_:str #Name of the model used to summarize the text
    topicClassificationModel_:str #Name of the model used to classify the text
        
    def __init__(self, webpageText):
        return 

    ###Setter methods
    def setSummarizerModel(self, summarizerModel:str):
        self.summarizerModel_ = summarizerModel
        return 
        
    def setTopicClassificationModel(self, topicClassificationModel:str):
        self.topicClassificationModel_ = topicClassificationModel
        return

    ###Getter methods
    def getSummaryOfText(self) -> str:
        return self.summaryOfText_
        
    def getOneSentenceSummary(self) -> str:
        return self.oneSentenceSummary_
        
    def getTopicOfText(self) -> str:
        return self.topic_
        