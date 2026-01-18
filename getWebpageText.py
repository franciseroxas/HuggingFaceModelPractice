from bs4 import BeautifulSoup
import requests
import numpy as np
import urllib3
from http.cookiejar import Cookie

from UrlEnum import UrlEnum
from UrlObject import UrlObject

def getWebpageText(UrlObject: UrlObject, chunkSize: int = 10000, requestSession = None, headers = None) -> str:
    #Retrive from the UrlObject the url and the type of url
    url = UrlObject.getUrl()
    typeOfUrl = UrlObject.getTypeOfUrl()
    
    #Variable to hold the webpage text
    webpageText = ""
    
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
    
    res = requestSession.get(url, headers = headers)
    
    ## Webpage Text Scraper For:
    ### Left Leaning
    #CNN
    if(typeOfUrl == UrlEnum.CNN):
        soup = BeautifulSoup(res.text, 'html.parser')
        webpageText = soup.get_text().replace('\n', " ")
        webpageText = webpageText[np.max([0, webpageText.find(" min read ")])::]
    
    #AP NEWS    
    elif(typeOfUrl == UrlEnum.AP_NEWS):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "RichTextStoryBody RichTextBody")
    
    #TORONTO STAR
    elif(typeOfUrl == UrlEnum.THESTAR):             
        #MAYBE WORKS WHEN COOKIES ARE SET IN THE SESSION
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = '<div class="subscriber-preview"><p>"')
        
    #NBC NEWS
    elif(typeOfUrl == UrlEnum.NBC_NEWS):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    #WSFU 
    elif(typeOfUrl == UrlEnum.WSFU):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    #The Morning Call
    elif(typeOfUrl == UrlEnum.MCALL):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.USATODAY):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.CNBC):
        webpageText = getWebpageTextStartingAtTitle_(res)
    
    elif(typeOfUrl == UrlEnum.ABC_NEWS):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.STARADVERTISER):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.TIME):
        webpageText = getWebpageTextStartingAtTitle_(res)
    
    ###Sports
    #ESPN
    elif(typeOfUrl == UrlEnum.ESPN):
        webpageText = getWebpageTextStartingAtTitle_(res)
    
    ### AI / Science Blogs
    #google research
    elif(typeOfUrl == UrlEnum.GOOGLE_RESEARCH):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "component-as-block --no-padding-top --theme-light --dbl-padding")
    
    #meta ai research
    elif(typeOfUrl == UrlEnum.META_AI_RESEARCH):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "minute read")
        
    #Microsoft ai research
    elif(typeOfUrl == UrlEnum.MICROSOFT_AI_BLOG):
        #Generic webpage text scraper 
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    #NVIDIA blog
    elif(typeOfUrl == UrlEnum.NVIDIA_BLOG):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "Reading Time:")
        
    elif(typeOfUrl == UrlEnum.NATURE):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.NASA):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    ###Center
    elif(typeOfUrl == UrlEnum.BOSTON_25_NEWS):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "<article class=")
        
    elif(typeOfUrl == UrlEnum.SKY_NEWS):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.BBC_NEWS):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.INVESTOPEDIA):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    ### Finance
    elif(typeOfUrl == UrlEnum.CNBC):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    ### Right
    elif(typeOfUrl == UrlEnum.GUARDIAN):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.THE_CENTER_SQUARE):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.NEWSWEEK):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.BOSTON_HERALD):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    elif(typeOfUrl == UrlEnum.THE_EPOCH_TIMES):
        webpageText = getWebpageTextStartingAtTitle_(res)
        
    ### Unknown Bias + Factuality
    elif(typeOfUrl == UrlEnum.USATODAY):
        webpageText = getWebpageTextStartingAt_(res, textToSkipTo = "gnt_em_vb gnt_em_vb__he")
        
    elif(typeOfUrl == UrlEnum.ALJAZEERA):
        webpageText = getWebpageTextStartingAtTitle_(res)
    
    elif(typeOfUrl == UrlEnum.TIME):
        webpageText = getWebpageTextStartingAtTitle_(res)
         
    #Other
    else:
        #Generic webpage text scraper 
        soup = BeautifulSoup(res.text, 'html.parser')
        webpageText = soup.get_text().replace('\n', " ")
        
        ArticleTitleTag = soup.find('title')
        if(ArticleTitleTag is not None):
            ArticleTitle = ArticleTitleTag.get_text()
            webpageText = webpageText[np.max([0, webpageText.find(" min read"), webpageText.find("minute read"), webpageText.find(ArticleTitle)])::]
        else:
            webpageText = webpageText[np.max([0, webpageText.find(" min read"), webpageText.find("minute read")])::]
    
    #Truncate the webpageText if it is too long due to compute
    webpageText = webpageText[0: min(len(webpageText), chunkSize)]
        
    return webpageText

### HELPER FUNCTIONS
def createSessionCookie_(version:int =0, 
                         name:str ='user_pref_currency', 
                         value:str ='CNY', 
                         port:any = None, 
                         port_specified:bool = False, 
                         domain:str = '.example.com', 
                         domain_specified:bool = True, 
                         domain_initial_dot:bool = True, 
                         path:str = '/', 
                         path_specified:bool = True, 
                         secure:bool = True, 
                         expires:int = 1701503561, 
                         discard:bool = True, 
                         comment:any = None, 
                         comment_url:any = None, 
                         rest:dict = {'HttpOnly': None}, 
                         rfc2109:bool = False):
    
    #Default values taken from 
    sessionCookie = Cookie(version=version, 
                           name=name, 
                           value=value, 
                           port=port, 
                           port_specified=port_specified, 
                           domain=domain, 
                           domain_specified=domain_specified, 
                           domain_initial_dot=domain_initial_dot, 
                           path=path, 
                           path_specified=path_specified, 
                           secure=secure, 
                           expires=expires, 
                           discard=discard, 
                           comment=comment, 
                           comment_url=comment_url, 
                           rest=rest, 
                           rfc2109=rfc2109)

    return sessionCookie
    
#A helper function to call to quickly unit test 
def getWebpageTextFromUrl_(url: str) -> str:
    return getWebpageText(UrlObject(url))
  
def getWebpageTextStartingAtTitle_(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    webpageText = soup.get_text().replace('\n', " ")
    
    ArticleTitleTag = soup.find('title')
    if(ArticleTitleTag is not None):
        ArticleTitle = ArticleTitleTag.get_text()
        webpageText = webpageText[np.max([0, webpageText.find(ArticleTitle)])::]
        
    return webpageText
  
#Helper functions to reduce redundant code:  
def getWebpageTextStartingAt_(res, textToSkipTo: str):
    #Html Text
    htmlText = res.text
    htmlText = htmlText.split('\n')
            
    #Flag to state when to add to webpage text
    addToTextFlag = False
    
    #Variable to hold the webpage text
    webpageText = ""
    
    for line in htmlText:
        if(len(line) == 0):
            continue
        elif(line.find(textToSkipTo) > -1):
            addToTextFlag = True
            
        if(addToTextFlag):
            webpageText = webpageText + line + " "
    
    #Intended to remove adverts, titles, hashtags that appear before the article.
    if(addToTextFlag):
        #Add everything starting from here and add it to the bs4 object
        soup = BeautifulSoup(webpageText, 'html.parser')
            
        #Get clean text
        webpageText = soup.get_text()
    
    #If the addToTextFlag is still false just use the html text and clean it up with bs4 as is.
    else:
        soup = BeautifulSoup(res.text, 'html.parser')
            
        #Get clean text
        webpageText = soup.get_text()
    
    return webpageText
    
if __name__ == "__main__":
    print(getWebpageTextFromUrl_('https://www.cnn.com/cnn-underscored/reviews/best-dyson-vacuums'))