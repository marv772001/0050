import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime,timedelta
from pathlib import Path

def loadCsv(path):
  df=pd.read_csv(path,encoding="utf8")
  return df
def process(df, origin):
        df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d') + pd.DateOffset(years=origin)
        for col in df.columns:
            if col=="漲跌幅":
               df[col]=df[col].str.strip("%").astype(float)/100
            elif col!="日期":
              df.loc[:, col] = df[col].apply(lambda x: float(x.replace(',', '') if type(x) == str else x)).values
        return df
def heatmap(df):
    df4Correlation = df.copy().drop(columns=['日期'])
    correlationDf = df4Correlation.corr()
    plt.figure(figsize=(25, 20))
    sns.heatmap(data=correlationDf, annot=True,fmt=".2f")
    date=df["日期"]
    startdate=date.iloc[0].strftime("%Y-%m-%d")
    enddate=date.iloc[-1].strftime("%Y-%m-%d")
    text=(f"Correlation Heatmap from {startdate} to {enddate}")
    plt.title(text)
    savePath =f"heatmap_{startdate}_{enddate}.png"
    plt.savefig(savePath)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
def splitbydate(df,num):
    for i in range(0,10000,num):
        start=i
        end=i+num
        final=57
        if end<final:
            newDF=df.iloc[start:end]
            heatmap(newDF)
    
    for i in range(58,10000,num):
        start=i
        end=i+num
        final=120
        if end<final:
            newDF=df.iloc[start:end]
            heatmap(newDF)            
     
DF1=loadCsv("0050漲跌幅.csv")
DF2=loadCsv("0050 三大法人2023 4-6-1 .csv")
DF3=loadCsv("0050股價.csv")
DF4=loadCsv("0050淨值.csv")
DF5=loadCsv("加權指數_2023.csv")
d=DF3["日期"]
for i in range(len(d)):
    d.iloc[i]=d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911))   
DF1=process(DF1,0)
DF2=process(DF2,0)
DF3=process(DF3,0)
DF4=process(DF4,0)
DF5=process(DF5,0)
DF2=DF2[["日期","成交量(張)","外資買賣進(張)","投信買賣超","自營商買賣超"]]
DF3=DF3[["日期","成交筆數"]]
DF_ALL=pd.merge(DF1,DF2,on="日期")
DF_ALL=pd.merge(DF_ALL,DF3,on="日期")
DF_ALL=pd.merge(DF_ALL,DF4,on="日期")
DF_ALL=pd.merge(DF_ALL,DF5,on="日期")
DF_ALL["大戶散戶"]=DF_ALL["成交量(張)"]/DF_ALL["成交筆數"]
DF_ALL.drop(DF_ALL.columns[DF_ALL.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
DF_ALL.to_csv("final.csv")
splitbydate(DF_ALL,5)
splitbydate(DF_ALL,7)
splitbydate(DF_ALL,10)



