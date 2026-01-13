import requests
from bs4 import BeautifulSoup
import urllib.request

def WebsiteParser():
    #Headers which tell bs4 what type of internet browser to use
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    
    #URL to access
    url = 'https://www.staradvertiser.com/tag/world-news/'
    
    #Setup to download the text from the webpage
    r = requests.get(url, timeout = 10, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    
    #Get all of the lines of text from the webpage
    lines = str(soup).split('\n')
        
    #TODO: Sort these in the order of the ENUMs in the URL objects
    if(url.find('www.cnn.com') > 0):
        links = parseCnnHomepage(lines)
    elif(url.find('guardian.com') > 0):
        links = parseGuardianHomepage(lines)
    elif(url.find('apnews.com') > 0):
        links = parseApNewsHomepage(lines)
    elif(url.find('research.google/blog') > 0):
        links = parseGoogleBlogHomepage(lines)
    elif(url.find('ai.meta.com') > 0):
        links = parseFacebookBlogHomepage(lines)
    elif(url.find('blogs.nvidia.com') > 0):
        links = parseNvidiaBlogHomepage(lines)
    elif(url.find('cnbc.com') > 0):
        links = parseAritraryHomepage(lines, 
                    url = 'https://www.cnbc.com/', 
                    skipAddingUrl = True, 
                    searchStrList = [str('class="LatestNews-headlineWrapper')], 
                    firstSubStrToFind = 'href="', 
                    secondSubStrToFind = '" title',
                    skipStrList = [""])
    elif(url.find('time.com') > 0):
        links = parseAritraryHomepage(lines,
                    url = 'https://time.com/', 
                    skipAddingUrl = True,
                    searchStrList = [str('duration-300 transition-colors')],
                    firstSubStrToFind = 'href="',
                    secondSubStrToFind = '">',
                    skipStrList = ["/section/"])
    elif(url.find('nature.com') > 0):
        links = parseAritraryHomepage(lines, 
                    url = 'https://www.nature.com', 
                    skipAddingUrl = False, 
                    searchStrList = [str('c-card__link')],
                    firstSubStrToFind = 'href="',
                    secondSubStrToFind = '" itemprop')
    #For the website:https://www.staradvertiser.com/tag/world-news/
    elif(url.find('staradvertiser.com/tag/world-news/') > 0):
        links = parseAritraryHomepage(lines, 
                    url = 'https://www.staradvertiser.com/', 
                    skipAddingUrl = True, 
                    searchStrList = [str('class="fw-bold"')],
                    firstSubStrToFind = 'href="',
                    secondSubStrToFind = '">Read more') 

    #Convert the set into a list for readability when accessing
    links = [link for link in links] 
    print(links)
    return

### Website specific functions to retrieve the individual article links 
def parseCnnHomepage(lines, url = 'https://www.cnn.com/'):
    #Create a set variable for all of the links on 
    links = set()
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        #Get the current html line as a character vector
        if(lines[i].find('data-link-type="article"')>0):
            currentArticleSuffix = lines[i][lines[i].find('href="/')+len('href="/'):lines[i].find('">')]
            #Add to the set 
            links.add(url+currentArticleSuffix)
    
    return links
    
def parseGuardianHomepage(lines, url = "https://www.theguardian.com/"):
    #Create a set variable for all of the links on 
    links = set()
    
    #Variables for the search string in the j loop
    searchStrNews = str('data-link-name="news')
    searchStrArticle = str('data-link-name="article')
    searchStrFeature = str('data-link-name="feature')
    
    #Preallocate variables to hold the indices of the articles in the text
    firstIdx = -1
    secondIdx = -1
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        #Get a variable to represent the current line
        currLine = str(lines[i])
        
        for j in range(len(currLine) - len(searchStrFeature)):            
            #Check if a news article, feature article or no article is found
            if(currLine[j:j+len(searchStrArticle)] == searchStrArticle or 
               currLine[j:j+len(searchStrFeature)] == searchStrFeature or
               currLine[j:j+len(searchStrNews)] == searchStrNews):
               
                #Get the indices of the article suffix
                firstIdx = j + currLine[j::].find('href="/') + len('href="/')
                secondIdx = j + currLine[j::].find('"><')
                
                #Add the article to the set
                links.add(url+currLine[firstIdx:secondIdx])
    
    return links
    
def parseApNewsHomepage(lines):
    #Create a variable for a set for all of the links on 
    links = set()
    searchStrLink = str('<a class="Link" href="')
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - len(searchStrLink)):
            #Get the current html line as a character vector
            if(currLine[j:j+len(searchStrLink)] == searchStrLink):
                firstIdx = j + len(searchStrLink) 
                secondIdx = currLine.find('"><')
                
                #If the end of the href link is not present, do not add this text to the st
                if(secondIdx != -1):
                   links.add(currLine[firstIdx:secondIdx])
    return links
    
def parseGoogleBlogHomepage(lines, url = "https://research.google"):
    #Create a variable for a set for all of the links on 
    links = set()
    searchStrGlueCard = str('class="glue-card not-glue" href="')
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - len(searchStrGlueCard)):
            #Get the current html line as a character vector
            if(currLine[j:j+len(searchStrGlueCard)] == searchStrGlueCard):
                firstIdx = j + len(searchStrGlueCard) 
                secondIdx = currLine.find('">')
                
                #If the end of the href link is not present, do not add this text to the st
                if(secondIdx != -1):
                   links.add(url + currLine[firstIdx:secondIdx])
    return links
    
def parseFacebookBlogHomepage(lines, url = 'https://ai.meta.com/blog/'):
    #Create a variable for a set for all of the links on 
    links = set()
    searchStrLink = str('"creative":"link","creative_detail":"link","create_type":"link","create_type_detail":"link"}')
    
    #Variable to hold the text that is possibly a link to a blog webpage
    possibleLink = ""
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        print(currLine)
        
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - len(searchStrLink)):
            #Get the current html line as a character vector
            if(currLine[j:j+len(searchStrLink)] == searchStrLink):
                firstIdx = currLine[j::].find('href="') + len('href="')
                secondIdx = currLine[j::].find('" id="u_0_') 
                
                #If the end of the href link is not present, do not add this text to the set
                if(secondIdx != -1):
                   possibleLink = currLine[j+firstIdx:j+secondIdx]
                else:
                   possibleLink = ""
                   continue
                   
                #These are all links or suffixes of links. Check if this is a blog or a link to an about page
                if(len(possibleLink) < len(url)):
                   possibleLink = ""
                   continue
                
                #This seems to be an edge case that links to a second blog page that no longer exists. Redirects back to the main blog page
                if(possibleLink.find('?page=2') > -1):
                   possibleLink = ""
                   continue
                   
                #This is a link to a blog article
                if(possibleLink[0:len(url)] == url):
                   links.add(possibleLink)
                   
                #Modify this at the end of the loop so that it does not pass the checks above 
                possibleLink = ""
    return links    
    
def parseNvidiaBlogHomepage(lines):
    links = set()
    searchStrReadMore = str('read-more')
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - len(searchStrReadMore)):
            #Get the current html line as a character vector
            if(currLine[j:j+len(searchStrReadMore)] == searchStrReadMore):
                firstIdx = j + currLine[j::].find('href="') + len('href="')
                secondIdx = j + currLine[j::].find('">')
                
                #Add the url to the set of links
                links.add(currLine[firstIdx:secondIdx])
    return links
    
def parseCnbcHomepage(lines, url = 'https://www.cnbc.com/'):
    links = set()
    
    searchStrHeadline = str('class="LatestNews-headlineWrapper')
    
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - len(searchStrHeadline)):
            #Get the current html line as a character vector
            if(currLine[j:j+len(searchStrHeadline)] == searchStrHeadline):
                firstIdx = currLine[j::].find('href="') + len('href="')
                secondIdx = currLine[j::].find('" title')
                
                #Remove the pro links
                possibleLink = currLine[j + firstIdx:j + secondIdx]
                
                #Remove references to the 'sports', 'business', etc... tabs
                if(len(possibleLink) < len(url)):
                    continue
                #Remove the 'about' pages
                elif(possibleLink[0:len(url)] != url):
                    continue
                #Add the url to the set of links
                links.add(currLine[j + firstIdx:j + secondIdx])
    
    return links
    
def parseAritraryHomepage(lines, url = "", skipAddingUrl = False, searchStrList = [""], firstSubStrToFind = "", secondSubStrToFind = "", skipStrList = [""]):
    #Create a set to hold the output of the links
    links = set()
    
    #Create a variable to hold the max length string that is being searched for
    maxSearchStrLen = len(searchStrList[0])
    for i in range(len(searchStrList)):
        maxSearchStrLen = max(maxSearchStrLen, len(searchStrList[i]))
        
    #Create a variable to hold the possible link
    possibleLink = ""
        
    #loop through all of the lines in lines
    for i in range(0, len(lines)):
        currLine = lines[i]
        
        #Create two pointers for iterating through the ith line
        firstIdx = -1
        secondIdx = -1
        
        #Check if the current line of text has a link in it 
        for j in range(len(currLine) - maxSearchStrLen):
            #Create a flag to look for a possible link
            hasPossibleLink = False
            
            #If any of the search strings are included in the current line at the current index continue
            for k in range(len(searchStrList)):
                searchStrCurrent = searchStrList[k]
                hasPossibleLink = hasPossibleLink or (currLine[j:j+len(searchStrCurrent)] == searchStrCurrent)
        
            #Continue if none are found
            if(hasPossibleLink):
                firstIdx = currLine[j::].find(firstSubStrToFind) + len(firstSubStrToFind)
                secondIdx = currLine[j::].find(secondSubStrToFind)
                
                possibleLink = currLine[j + firstIdx:j + secondIdx]
            else:
                continue
                
            #Url is already included in the text    
            if(skipAddingUrl):
                #Remove references to the 'sports', 'business', etc... tabs
                if(len(possibleLink) < len(url)):
                    continue
                #Remove the 'about' pages
                elif(possibleLink[0:len(url)] != url):
                    continue

                #Add the url to the set of links
                links.add(currLine[j + firstIdx:j + secondIdx])
                
            #Url is not included in the text and needs to be added
            else:
                #This if for edge cases that need to be skipped
                for k in range(len(skipStrList)):
                    skipStr = skipStrList[k]
                    if(len(skipStr) > 0 and 
                        possibleLink.find(skipStr) > -1):
                       possibleLink = ""
                       continue
            
                links.add(url + currLine[j + firstIdx:j + secondIdx])
                
    return links
    
def linesToText(lines):
    with open('debugHtmlCopy.txt', 'a') as file:
        for line in lines:
            file.write(line + '\n')
    return 

#https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

if __name__ == "__main__":
    WebsiteParser()