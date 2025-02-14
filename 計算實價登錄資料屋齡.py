# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:18:26 2023

@author: FST
"""
import pandas as pd
from tqdm import tqdm
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")



#計算屋齡
import datetime
date = []
# 设置起始日期和结束日期
start_date = datetime.date(1, 1, 1)
end_date = datetime.date(1, 12, 31)

# 生成并打印所有月份和日期的4位数字
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%m%d")
    date.append(date_str)
    current_date += datetime.timedelta(days=1)
    

external_df = pd.read_csv("../外部資料集/實價登錄資料.csv")    

external_df["建築完成年月"] = external_df["建築完成年月"].astype(str)
external_df["建築完成年月"] = external_df["建築完成年月"].apply(lambda x: x[:-4]+"0228" if x[-4:]=="0229" else x)
external_df["建築完成年月"] = external_df["建築完成年月"].apply(lambda x: x[:-4]+"0101" if x[-4:]=="0000" else x)
external_df["建築完成年月"] = external_df["建築完成年月"].apply(lambda x: x[:-2]+"01" if x[-2:]=="00" else x)

external_df["交易年月日"] = external_df["交易年月日"].astype(str)
external_df["交易年月日"] = external_df["交易年月日"].apply(lambda x: x[:-4]+"0228" if x[-4:]=="0229" else x)
external_df["交易年月日"] = external_df["交易年月日"].apply(lambda x: x[:-4]+"0101" if x[-4:]=="0000" else x)
external_df["交易年月日"] = external_df["交易年月日"].apply(lambda x: x[:-2]+"01" if x[-2:]=="00" else x)

pattern = r'^[-+]?[0-9]+$'

external_df['交易年月日_%y%m%d'] = external_df['交易年月日'].astype(str)
is_integer = external_df['交易年月日_%y%m%d'].str.match(pattern)
external_df['交易年月日_%y%m%d'] = external_df['交易年月日_%y%m%d'].where(is_integer, "")
external_df['交易年月日_%y%m%d'] = external_df['交易年月日_%y%m%d'].apply(lambda x: (str(int(x[:3])+1911)[2:]+x[3:] if len(x) == 7 else str(int(x[:2])+1911)[2:]+x[2:]) if len(x)>=6 else "")
external_df['交易年月日_match_format'] = external_df['交易年月日_%y%m%d'].apply(lambda x: True if x[2:] in date else False)

external_df['建築完成年月_%y%m%d'] = external_df['建築完成年月'].astype(str).apply(lambda x: x.split(".")[0])
is_integer = external_df['建築完成年月_%y%m%d'].str.match(pattern)
external_df['建築完成年月_%y%m%d'] = external_df['建築完成年月_%y%m%d'].where(is_integer, "")
external_df['建築完成年月_%y%m%d'] = external_df['建築完成年月_%y%m%d'].apply(lambda x: (str(int(x[:3])+1911)[2:]+x[3:] if len(x) == 7 else str(int(x[:2])+1911)[2:]+x[2:]) if len(x)>=6 else "")
external_df['建築完成年月_match_format'] = external_df['建築完成年月_%y%m%d'].apply(lambda x: True if x[2:] in date else False)

external_df['match_format'] = (external_df['交易年月日_match_format'] & external_df['建築完成年月_match_format'])

external_df1 = external_df[external_df['match_format']==True]
external_df2 = external_df[external_df['match_format']==False]


external_df1['交易年月日_%y%m%d'] = pd.to_datetime(external_df1['交易年月日_%y%m%d'], format='%y%m%d')
external_df1['建築完成年月_%y%m%d'] = pd.to_datetime(external_df1['建築完成年月_%y%m%d'], format='%y%m%d')

external_df1['屋齡'] = (external_df1['交易年月日_%y%m%d'] - external_df1['建築完成年月_%y%m%d']).dt.days / 365

external_df1.loc[(external_df1['交易年月日'].astype(float) > external_df1['建築完成年月'].astype(float)) & (external_df1['屋齡'].astype(float)<0), '屋齡'] += 100
external_df1.loc[external_df1['交易年月日'].astype(float) < external_df1['建築完成年月'].astype(float), '屋齡'] = None

external_df1.loc[external_df1['交易年月日'].astype(float) < external_df1['建築完成年月'].astype(float), '預售屋'] = True
external_df1.loc[(external_df1['屋齡']==0), '預售屋'] = None

external_df = pd.concat([external_df1, external_df2])   

external_df.to_csv("../外部資料集/實價登錄資料.csv",index=False)    
  

