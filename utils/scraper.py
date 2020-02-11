import numpy as np
import pandas as pd
import requests, json, time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from spellchecker import SpellChecker

def getJobDescription(url):
    """
    Sends a HTTP request to get the job description from the given URL

    Args:
        url (string) : The URL where the job advert is located

    Returns: 
        text (string) : The parsed text of the web page
    """

    url = url

    # https://medium.com/@mikelcbrowne/running-chromedriver-with-python-selenium-on-heroku-acc1566d161c
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    # set headless option
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    options.binary_location = GOOGLE_CHROME_PATH
    
    # initialise webdriver 
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    driver.get(url)
    time.sleep(3)

    # scrape web page
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")

    # parse page and remove script tags etc
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.getText()

    return text

def getWords(text):
    """
    Parses text and returns a list of words using NLTK

    Args:
        text (string) : The text string that will be parsed for words

    Returns: 
        verbs, adjectives, adverbs, nouns (lists) : The returned list of words
    """

    # tokenize text
    tokens = word_tokenize(text)

    # remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    words = []
    for w in tokens: 
        if w.lower() not in stop_words and w.lower().isalpha():
            words.append(w.lower())

    # remove misspelled words
    spell = SpellChecker()
    misspelled = spell.unknown(words=words)
    words_set = set()
    for w in words:
        if w not in misspelled:
            words_set.add(w)

    # add pos tags
    pos_words = nltk.pos_tag(words_set)

    # find all verbs, adj and adverbs
    # https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
    verbs = set()
    adjectives = set()
    nouns = set()
    adverbs = set()
    for word, pos_code in pos_words:
        if pos_code == 'NN':
            nouns.add(word)
        elif pos_code in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            verbs.add(word)
        elif pos_code in ['JJ', 'JJR', 'JJS']:
            adjectives.add(word)
        elif pos_code in ['RB', 'RBR', 'RBS']:
            adverbs.add(word)
    
    return list(verbs), list(adjectives), list(adverbs), list(nouns) 
