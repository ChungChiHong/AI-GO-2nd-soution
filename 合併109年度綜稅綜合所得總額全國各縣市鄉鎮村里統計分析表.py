# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:47:04 2023

@author: foresight
"""

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

extra_df = pd.read_csv('../外部資料集/109年度綜稅綜合所得總額全國各縣市鄉鎮村里統計分析表.csv')
#extra_df_group = extra_df[extra_df["村里"]=="合計"].drop(columns ="村里")
extra_df_each = extra_df[extra_df["村里"]!="合計"]
extra_df_each["村里"] = extra_df_each["鄉鎮市區"] +extra_df_each["村里"] 


for t in [0]:
    
    if t==0:
        df = pd.read_csv("../外部資料集/Training Dataset.csv")
    elif t==1:
        df = pd.read_csv("../外部資料集/Public Dataset.csv")
    else:
        df = pd.read_csv("../外部資料集/Private Dataset.csv")

    df["縣市"] =  df["縣市"].apply(lambda x: x.replace("台","臺") )
    df["鄉鎮市區"] = df["縣市"] + df["鄉鎮市區"] 
        

    df["村里"] = df["鄉鎮市區"] +df["村里"] 

    df = df.drop(columns ="鄉鎮市區")
    
    df = pd.merge(df, extra_df_each, on='村里', how='left')#.drop(columns ="鄉鎮市區")

    
    if t==0:
        df.to_csv("../外部資料集/Training Dataset.csv",index=False)
    elif t==1:
        df.to_csv("../外部資料集/Public Dataset.csv",index=False)
    else:
        df.to_csv("../外部資料集/Private Dataset.csv",index=False)    
        