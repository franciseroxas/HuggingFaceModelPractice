import string
from bs4 import BeautifulSoup
import requests

from UrlEnum import UrlEnum

class UrlObject:
    url_: str
    typeOfUrl_: UrlEnum.OTHER
    
    def __init__(self, url: str, typeOfUrl: UrlEnum = UrlEnum.OTHER):
        self.url_ = url
        self.typeOfUrl_ = typeOfUrl
        
    def getUrl(self) -> str:
        return self.url_
        
    def getTypeOfUrl(self) -> str:
        return self.typeOfUrl_
        