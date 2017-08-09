
# coding: utf-8

# In[32]:

import pandas as pd
import requests
import json
import demjson
import pymysql
from sqlalchemy import create_engine


# In[104]:

class csyyCrawler():
    headers = {"Tingyun_Process": "true",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; LON-AL00 Build/KTU84P)",
                   "Host": "m.csyeye.com",
                   "Connection": "Keep-Alive",
                   "Accept-Encoding": "gzip"}
    logindata = {"client_type":"android",
                 "net_type":"wifi",
                 "resolution":"810*1440",
                 "uuid":"867156854177351",
                 "system_version":"4.4.4",
                 "client_version":"4.8.8"}
    def getHtml(self,url):
        res = requests.post(url=url,headers=headers,data=logindata,verify=False)
        rawhtml = res.content.decode("utf-8")
        rawObj = demjson.decode(rawhtml)
        return rawObj
    
    def getProductRate(self):
        url = "https://m.csyeye.com/nnapp/index/product"
        rawObj = self.getHtml(url)
        index = ["product_code","product_name","year_rate","raise_money","lock_days"]
        df = pd.DataFrame(rawObj['data']).loc[:,index]
        df["year_rate"] = df["year_rate"].astype("float32")
        df[["raise_money","lock_days"]] = df[["raise_money","lock_days"]].astype("int32")
        return df
    def getGeneralInfo(self):
        url = "https://m.csyeye.com/nnapp/index/data_statistics"
        rawObj = self.getHtml(url)
        dailyIndex = ["investment","investment_amount"]
        reportIndex = ["enrollment","investment"]
        changeIndex = ["acc_"+x for x in reportIndex]
        dfDaily = pd.DataFrame(rawObj['data']['daily'],index=[0]).loc[:,dailyIndex]
        dfReport = pd.DataFrame(rawObj['data']['report'],index=[0]).loc[:,reportIndex]
        dfReport =  dfReport.rename(columns=dict(zip(reportIndex,changeIndex)))
        df = pd.concat([dfDaily,dfReport],axis=1)
        df = df.applymap(lambda x :x.replace(",",""))
        df = df.astype("int32")
        return df
    
    def insert_result(self,df,conn_info,dataLabel="rate"):
        dataLabel = dataLabel.lower()
        tabledict = {"rate":"csyy_product","general":"csyy_general"}
        tablename = tabledict.get(dataLabel)
        try:
            df.to_sql(name=tablename,con=conn_info, if_exists="append", index=False)
            print("success!")
        except:
            print("warning! insert unsuccessfully!") 


# In[86]:

local_con = create_engine("mysql+pymysql://root:871226@localhost:3306/yinker?charset=utf8")


# In[105]:

csyyCrawler = csyyCrawler()
rateInfo = csyyCrawler.getProductRate()
generalInfo = csyyCrawler.getGeneralInfo()
csyyCrawler.insert_result(rateInfo,conn_info=local_con,dataLabel="rate")
csyyCrawler.insert_result(generalInfo,conn_info=local_con,dataLabel="general")

