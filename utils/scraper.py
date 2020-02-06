import numpy as np
import pandas as pd
import requests, json, time
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

def getJobDescription(url):
    """
    Sends a HTTP request to get the job description from the given URL

    Args:
        url (string) : The URL where the job advert is located

    Returns: 
        text (int) : The parsed text of the web page
    """

    url = url

    # set headless option
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 

    # initialise webdriver 
    driver = webdriver.Chrome(r'utils\chromedriver.exe', options=options)
    driver.get(url)
    time.sleep(3)

    # scrape web page
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")

    # parse page and remove script tags etc
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = (soup.getText()).replace('?', ' ').replace('.', ' ').replace(',', ' ').replace(':', ' ').replace('\n', ' ')

    # split text on spaces
    print(visible_text.split(' '))

    


    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    #r = requests.get(url, headers=headers, verify=False, allow_redirects=True)
    #source = r.text
    #text = BeautifulSoup(source, 'lxml').get_text

    #rating = soup.find('span', {'class' : 'result'})
    #rating = rating.findAll('span')
    #rating = str(rating[-3].contents[0]).strip()


# TESTS
getJobDescription('https://www.monster.co.uk/jobs/l-sheffield,-yorkshire.aspx?jobid=215473959')

#getJobDescription('https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWNsYXNzPUpvYnMmb3duZXI9NTA3MDAwMCZzZWFyY2hfc2xpY2VfY3VycmVudD0xJm93bmVydHlwZT1mYWlyJnBhZ2VhY3Rpb249dmlld3ZhY2J5am9ibGlzdCZ1c2Vyc2VhcmNoY29udGV4dD05MzkxMzM0NyZqb2JsaXN0X3ZpZXdfdmFjPTE2NjM0MjEmY3NvdXJjZT1jc3FzZWFyY2gmcmVxc2lnPTE1ODEwMjQxMzQtOTcxMTBmMzA2NDY1ZjRmNDAxNzYwYWFjYTU5YjYxMTc3M2VmNzMwOA==')

#getJobDescription('https://www.monster.co.uk/jobs/l-sheffield,-yorkshire.aspx?jobid=215131987')

