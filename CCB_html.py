
# coding: utf-8

import pandas as pd
import numpy as np
import requests
import json
import time

def getCCBProd():
    def getObj(url, index, params = {'queryForm.provinceId': '440', 'queryForm.brand': '03', 'pageNo': '1'}):
        # 获取总条数
        repStrap = requests.post(url, data=params)
        rawObjStrap = json.loads(repStrap.text)
        params['pageSize'] = rawObjStrap['totalCount']

        rep = requests.post(url, data=params)
        rawObj = json.loads(rep.text)
        dataObj = rawObj['ProdList']
        df = pd.DataFrame(dataObj)
        df = df.ix[:, index]
        return df

    def timeShift(x):
        if(np.isnan(x)):
            a = ""
        else:
            a = time.strftime(timeFormat, time.localtime(x/1000))
        return a

    index = ['code', 'name', 'yieldRate', 'purFloorAmt', 'investPeriod', 'collBgnDate', 'collEndDate']
    change = {'code': 'prodID', 'name': 'title', 'yieldRate': 'rate', 'purFloorAmt': 'leastInvest',\
              'investPeriod': 'periodDays', 'collBgnDate': 'beginDate', 'collEndDate': 'endDate'}
    provinceDict = {'110': 'Beijing', '440': 'Guangdong', '310': 'Shanghai'}
    provinceCodeList = list(provinceDict.keys())
    url = 'http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp'
    params = {'queryForm.brand': '03', 'pageNo': '1'}
    result = pd.DataFrame()
    for province in provinceCodeList:
        params['queryForm.provinceId'] = province
        tmp = getObj(url=url, params=params, index=index)
        tmp['city'] = provinceDict[province]
        result = result.append(tmp)
    timeFormat = "%Y-%m-%d %H:%M:%S"
    result['log_time'] = time.strftime(timeFormat, time.localtime())
    result['collBgnDate'] = result['collBgnDate'].apply(lambda x: timeShift(x))
    result['collEndDate'] = result['collEndDate'].apply(lambda x: timeShift(x))
    result.rename(columns=change, inplace=True)

    return(result)

if(__name__ == '__main__'):
    print(getCCBProd())

