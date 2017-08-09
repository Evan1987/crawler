
# coding: utf-8
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import requests
import json

def getObj(url,page):
    url = url+"pageIndex="+str(page)
    rep = requests.get(url)
    html = rep.text.encode(rep.encoding).decode('utf-8')
    rawObj = json.loads(html)
    dataObj = rawObj['data']
    loanObj = dataObj['loans']
    index = ['loanId','title','interest','amount','months','status','beginBidTime']
    df = pd.DataFrame(loanObj)
    df = df.ix[:,index]
    return df

url = 'https://www.renrendai.com/loan'
trueUrl ="https://www.renrendai.com/lend/loanList!json.action?"
rep = requests.get(url=url)
rawhtml = rep.text.encode(rep.encoding).decode('utf-8')
soup = BeautifulSoup(rawhtml,'lxml')
targetTag = soup.find(type = re.compile('json'))
rawObj = json.loads(targetTag.text)
dataObj = rawObj['data']
totalPage = int(dataObj['totalPage'])
result = pd.DataFrame()

for page in range(1,totalPage+1):
    tmp = getObj(trueUrl,page)
    result = result.append(tmp)

result.to_csv("F:/result.csv")


