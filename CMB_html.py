
# coding: utf-8

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import demjson
import re

def getCMBProd():

    def getCMBObj(url,pagesize=1):
        def getHtml(rawhtml):
            begin = rawhtml.find("{")
            end = rawhtml.rfind("}")+1
            return rawhtml[begin:end]
        rep = requests.get(url+str(pagesize))
        rawhtml = rep.text.encode(rep.encoding).decode(rep.encoding)
        html = getHtml(rawhtml)
        rawObj = demjson.decode(html)
        return rawObj

    index = ['PrdCode', 'PrdName', 'NetValue', 'InitMoney', 'FinDate', 'BeginDate', 'EndDate']
    change = {'PrdCode': 'prodID', 'PrdName': 'title', 'NetValue': 'rate', 'InitMoney': 'leastInvest', 'FinDate': 'periodDays', 'BeginDate': 'beginDate', 'EndDate': 'endDate'}
    timeFormat = "%Y-%m-%d %H:%M:%S"
    url = 'http://www.cmbchina.com/cfweb/svrajax/product.ashx?op=search&currency=10&salestatus=A&series=01&pageindex=1&pagesize='

    # 获取总条数
    rawObj = getCMBObj(url, pagesize=1)
    totalRecord = int(rawObj['totalRecord'])

    rawObj = getCMBObj(url, pagesize=totalRecord)
    df = pd.DataFrame(rawObj['list'])
    df = df.ix[:, index]
    df = df[df.NetValue.apply(len) > 1]
    df['NetValue'] = df['NetValue'].apply(lambda x: int(re.sub('\D', '', x))/100)
    df['FinDate'] = df['FinDate'].apply(lambda x: int(re.sub('\D', '', x)))
    df['log_time'] = time.strftime(timeFormat, time.localtime())
    df.rename(columns=change, inplace=True)
    return df

if(__name__ == '__main__'):
    print(getCMBProd())
