
# coding: utf-8

# In[95]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import json


# In[147]:

def getJindanRate():
    url = "https://bapi.jindanlicai.com/v10"
    headers = {"Content-Type":"application/json; charset=utf-8",
               "Host":"bapi.jindanlicai.com",
               "Connection":"Keep-Alive",
               "Accept-Encoding":"gzip",
               "User-Agent":"okhttp/2.7.5",
               "Content-Length":"446"
              }
    logindata = '''{"version":"2",
                  "statics":{"version":"6.1.1",
                             "ua":"HUAWEI MT7-TL10",
                             "os":"android6.0",
                             "system_version":"6.0",
                             "connecttype":"",
                             "device_token":"865164027661808",
                             "mobile":"",
                             "channel":"huawei",
                             "simnumber":"",
                             "imsi":"",
                             "udid":"669C5A287B482D4ABB22681FAC66903E",
                             "push_channelid":"3942943085421651425",
                             "push_userid":"996290184214211975",
                             "push_appid":"5336588",
                             "user_id":"",
                             "userKey":"",
                             "token":"",
                             "o7":""},
                "fun":{"get_total_amount":{},
                       "productList":{}}}'''
    res = requests.post(url=url,data=logindata,headers=headers,verify=False)
    jsonObj = json.loads(res.content)
    productList = jsonObj['productList']
    products = productList['data'][0]['data']
    index = ["pId","title","rate"]
    df = pd.DataFrame(products).loc[:,index]
    return df


# In[148]:

getJindanRate()

