import numpy as np
import pandas as pd
import requests, json, time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getApprovalRating(primeMinister):
    """
    Sends a HTTP request to get current PM's approval rating from YouGov

    Args:
        None

    Returns: 
        rating (int) : The current approval rating
    """

    url = "http://yougov.co.uk/topics/politics/explore/public_figure/" + primeMinister
    headers = {"User-Agent":"Mozilla/5.0"}
    r = requests.get(url, headers=headers, allow_redirects=True)
    source = r.text
    soup = BeautifulSoup(source, 'lxml')
    rating = soup.find('span', {'class' : 'result'})
    rating = rating.findAll('span')
    rating = str(rating[-3].contents[0]).strip()
    return rating