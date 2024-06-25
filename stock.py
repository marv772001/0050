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
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    
    sns.heatmap(data=correlation, annot=True,fmt=".2f")
    
    date = raw_data["日期"]
    startdate = date.iloc[0].strftime("%Y-%m-%d")
    enddate = date.iloc[-1].strftime("%Y-%m-%d")
    text = f"correlation Heatmap from {startdate} to {enddate}"
    savePath = f"heatmap_{startdate}_{enddate}.png"
    
    plt.title(text)
    plt.savefig(savePath)
    
def split_by_date(df: DataFrame,num: int) -> None:
    # from 4/1 to 6/30
    for i in range(0, 10000, num):
        start = i
        end = i + num
        final = 57 # the index of 10 month is 57
        if end < final:
            new_df = df.iloc[start:end]
            create_heatmap(new_df)

    # from 10/1 to 12/31
    for i in range(58, 10000, num):
        start = i
        end = i + num
        final = 120 # the index of the last date
        if end < final:
            new_df = df.iloc[start:end]
            create_heatmap(new_df)   
            

if __name__ == "__main__":
    data_base_path = "data"
    DF1 = load_csv(Path(data_base_path, "0050漲跌幅.csv"))
    DF2 = load_csv(Path(data_base_path, "0050 三大法人2023 4-6-1 .csv"))
    DF3 = load_csv(Path(data_base_path, "0050股價.csv"))
    DF4 = load_csv(Path(data_base_path, "0050淨值.csv"))
    DF5 = load_csv(Path(data_base_path, "加權指數_2023.csv"))
    
    # from 民國 to 西元
    d = DF3["日期"]
    for i in range(len(d)):
        d.iloc[i] = d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911)) 
        
    DF1 = to_float(DF1)
    DF2 = to_float(DF2)
    DF3 = to_float(DF3)
    DF4 = to_float(DF4)
    DF5 = to_float(DF5)  
    
    DF2 = DF2[["日期","成交量(張)","外資買賣進(張)","投信買賣超","自營商買賣超"]]
    DF3 = DF3[["日期","成交筆數"]]

    DF_ALL = pd.merge(DF1, DF2, on="日期").merge(DF3, on = "日期").merge(DF4, on = "日期").merge(DF5, on = "日期")

    DF_ALL["大戶散戶"] = DF_ALL["成交量(張)"] / DF_ALL["成交筆數"]
    DF_ALL.drop(DF_ALL.columns[DF_ALL.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    DF_ALL.to_csv("final.csv")

    split_by_date(DF_ALL, 5)
    split_by_date(DF_ALL, 7)
    split_by_date(DF_ALL, 10)



