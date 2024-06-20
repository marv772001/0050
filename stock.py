import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import seaborn as sns
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
def heatmap(df,start,end):
    df4Correlation = DF_ALL.copy().drop(columns=['日期'])
    correlationDf = df4Correlation.corr()
    plt.figure(figsize=(25, 20))
    sns.heatmap(data=correlationDf, annot=True,fmt=".2f")
    text=(f"Correlation Heatmap from {start} to {end}")
    plt.title(text)
    savePath = "heatmap_{start}_{end}.png"
    plt.savefig(savePath)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


            
     
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
DF_ALL.to_csv("final.csv",index=0)

temp=DF_ALL["日期"]
for i in temp[::5]:
    start=i
    end=i+timedelta(days=6)
    final=datetime.strptime("2024-06-30","%Y-%m-%d")
    if end<final:
        newDF=DF_ALL[(DF_ALL["日期"]>=start)&(DF_ALL["日期"]<=end)]
        heatmap(newDF,start,end)

# new_DS.plot(x="收盤價",y="漲跌價",kind="scatter")
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 使用中文字體

# for i,j in zip(DS["交易日期"],DS["收盤價"]):
#   if i>='2023/3/1' and i<'2023/3/10':
#      list_data.append(j)
# print(list_data)    