from enum import Enum

#Used to search through the function getWebpageText faster
#complex valued so that I can add to each list without having to renumber all sections
class UrlEnum(Enum):
    ###Left Leaning
    CNN = 1
    AP_NEWS = 2
    THE_INDEPENDENT = 3
    THESTAR = 4 #Needs cookie support 
    TORONTOSTAR = 4 #Same website as thestar 
    NBC_NEWS = 5
    WSFU = 6
    MCALL = 7
    USATODAY = 8
    CNBC = 9
    ABC_NEWS = 10
    STARADVERTISER = 11
    TIME = 12
    
    ###Science / Factual
    GOOGLE_RESEARCH = 1j
    META_AI_RESEARCH = 2j
    MICROSOFT_AI_BLOG = 3j
    NVIDIA_BLOG = 4j
    NATURE = 5j
    MIT_NEWS = 6j
    NASA = 7j
    
    ###Right
    GUARDIAN = -1
    THE_CENTER_SQUARE = -2
    NEWSWEEK = -3
    BOSTON_HERALD = -4
    THE_EPOCH_TIMES = -5
    
    ###Center
    BOSTON_25_NEWS = -1j
    SKY_NEWS = -2j
    BBC_NEWS = -3j
    INVESTOPEDIA = -4j 
    
    ###Finance Only
    YAHOO_FINANCE = -1-1j
    # elfinanciero - Spanish to English
    
    ###Sports
    ESPN = 1+1j
    
    ###Gaming / Entertainment
    IGN = -1+1j
    GAMESPOT = -2+2j
    
    ###Dont work without a javascript solution
    #INVESTING_COM = 
    #POLITICO = 
    #NYT
    #FORBES
    #Science.org
    #REUTERS
    
    ###Dont work due to CloudFront layer or similar
    #SEATTLE TIMES
    
    ### NEED TO TRANSLATE TO ENGLISH WITH ANOTHER MODEL
    # elfinanciero - Spanish to English

    ### MIXED FACTUALITY / Left Bias
    ALJAZEERA = 1.1
    
    ###Unknown
    OTHER = 0.1