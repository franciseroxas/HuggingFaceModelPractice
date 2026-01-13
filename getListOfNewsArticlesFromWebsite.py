from bs4 import BeautifulSoup
import requests
import numpy as np
import urllib3
from http.cookiejar import Cookie

from UrlEnum import UrlEnum
from UrlObject import UrlObject

#Returns a list of news articles from a website given a UrlObject
def getListOfNewsArticlesFromWebsite(UrlObject: UrlObject, maxSizeOfList: int = 10) -> list:
    listOfArticles = ["" for i in range(maxSizeOfList)] #Preallocate this to save time
    return listOfArticles