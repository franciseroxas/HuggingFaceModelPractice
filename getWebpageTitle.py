from bs4 import BeautifulSoup
import requests
import numpy as np
import urllib3
from http.cookiejar import Cookie

from UrlEnum import UrlEnum
from UrlObject import UrlObject

def getWebpageTitle(UrlObject: UrlObject, requestSession = None, headers = None) -> str:
    #Retrive from the UrlObject the url and the type of url
    url = UrlObject.getUrl()    
        
    if(headers is None):
        headers = {
        'user-agent': 'My app',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',}
        
    if(requestSession is None):        
        #Request object
        requestSession = requests.session()
    
    #Get the html content
    res = requestSession.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
	
    #Variable to hold the title text
    titleText = soup.title.text
    
    return titleText