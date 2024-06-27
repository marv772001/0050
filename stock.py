import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from pathlib import Path

def load_csv(path: str) -> DataFrame:
    return pd.read_csv(path, encoding="utf-8")

def to_float(df: DataFrame) -> DataFrame:
    df["日期"] = pd.to_datetime(df["日期"], format="%Y/%m/%d")
    for col in df.columns:
        if col == "漲跌幅":
            df[col] = df[col].str.strip("%").astype(float) / 100
        elif col != "日期":
            df.loc[:, col] = df[col].apply(lambda x: float(x.replace(',', '') if type(x) == str else x)).values
    return df

def create_heatmap(raw_data: DataFrame) -> None:
    correlation = raw_data.copy().drop(columns=["日期"]).corr()
    
    # setup the figure size before draw the figure
    plt.figure(figsize=(25, 20))
    sns.heatmap(data=correlation, annot=True,fmt=".2f")
    date = raw_data["日期"]
    startdate = date.iloc[0].strftime("%Y-%m-%d")
    enddate = date.iloc[-1].strftime("%Y-%m-%d")
    text = f"correlation Heatmap from {startdate} to {enddate}"
    savePath = f"heatmap_{startdate}_{enddate}.png"
    plt.title(text)
    plt.savefig(savePath)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
   


   
  
def split_by_date(df: DataFrame,num: int) -> None:
    # from 4/1 to 6/30
    for i in range(0,10000,num):
        start = i
        end = i + num
        final = 57
        if end < final:
            newDF = df.iloc[start:end]
            #heatmap(newDF)
            df4Correlation2 = newDF.copy().drop(columns=['日期'])    
            correlationDf2 = df4Correlation2.corr()  
            correlationDf2.reset_index(inplace=True)
            new=correlationDf2.iloc[2:3]
            if i == 0:
                new1 = new
            else:
                new1 = new1._append(new,ignore_index=True) 
    new1.drop(["index","收盤價","漲跌價","漲跌幅"],inplace=True, axis=1)              
    new1.to_csv(f"456 {num} days.csv")
    new1 = pd.DataFrame()
    # from 10/1 to 12/31
    for i in range(58,10000,num):
        start = i
        end = i + num
        final = 120
        if end < final:
            newDF = df.iloc[start:end] 
            #heatmap(newDF)  
            df4Correlation2 = newDF.copy().drop(columns=['日期']) 
            correlationDf2 = df4Correlation2.corr()  
            correlationDf2.reset_index(inplace=True)
            new = correlationDf2.iloc[2:3]
            if i == 58:
                new1 = new
            else:
                new1 = new1._append(new,ignore_index=True) 
    new1.drop(["index","收盤價","漲跌價","漲跌幅"],inplace=True, axis=1)             
    new1.to_csv(f"101112 {num} days.csv")               

if __name__ == "__main__":
    data_base_path = "data"
    DF1 = load_csv(Path(data_base_path, "0050漲跌幅.csv"))
    DF2 = load_csv(Path(data_base_path, "0050 三大法人2023 4-6-1 .csv"))
    DF3 = load_csv(Path(data_base_path, "0050股價.csv"))
    DF4 = load_csv(Path(data_base_path, "0050淨值.csv"))
    DF5 = load_csv(Path(data_base_path, "加權指數_2023.csv"))
    DF6 = load_csv(Path(data_base_path,"NASDAQ_2023 (1).csv"))
    trenddf= load_csv (Path(data_base_path,"googld trend 0050.csv"))
    trenddf['日期'] = pd.to_datetime(trenddf['日期'])
    trenddf.set_index('日期', inplace=True)
    date_range = pd.date_range(start=trenddf.index.min(), end=trenddf.index.max(), freq='D')
    trenddf = trenddf.reindex(date_range)
    trenddf = trenddf.interpolate(method='linear')
    trenddf.reset_index(inplace=True)
    trenddf.rename(columns={'index': '日期'}, inplace=True)
    # from 民國 to 西元
    d = DF3["日期"]
    for i in range(len(d)):
        d.iloc[i] = d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911)) 
        
    DF1 = to_float(DF1)
    DF2 = to_float(DF2)
    DF3 = to_float(DF3)
    DF4 = to_float(DF4)
    DF5 = to_float(DF5)  
    DF6 = to_float(DF6)
    DF2 = DF2[["日期","成交量(張)","外資買賣進(張)","投信買賣超","自營商買賣超"]]
    DF3 = DF3[["日期","成交筆數"]]
    DF6=DF6[["日期","nasdaQ Close","nasdaQ Volume","SP 500 Close","SP 500 Volume"]]
    DF_ALL = pd.merge(DF1, DF2, on="日期").merge(DF3, on = "日期").merge(DF4, on = "日期").merge(DF5, on = "日期").merge(trenddf,on="日期").merge(DF6, on = "日期")
    DF_ALL["大戶散戶比例"] = DF_ALL["成交量(張)"] / DF_ALL["成交筆數"]
    DF_ALL.drop(DF_ALL.columns[DF_ALL.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    DF_ALL.to_csv("final.csv")

    split_by_date(DF_ALL, 5)
    split_by_date(DF_ALL, 7)
    split_by_date(DF_ALL, 10)



