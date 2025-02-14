# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:18:20 2023

@author: user
"""


import pandas as pd
from tqdm import tqdm
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def number_to_chinese(num):
    chinese_numerals = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    unit_positions = ['', '十', '百', '千']

    if num < 0 or num > 9999:
        return "數字範圍應在1到9999之間"

    result = ""
    digits = [int(d) for d in str(num).zfill(4)]

    for i in range(4):
        digit = digits[i]
        if digit != 0:
            result += chinese_numerals[digit] + unit_positions[4 - i - 1]

    # 處理 "一十" 的情況
    result = result.replace('一十', '十')

    return result

def generate_integer_list(n):
    if n <= 1:
        return "輸入的正整數必須大於1"
    
    # 計算範圍
    start = max(2, n - 3)
    end = n + 4
    
    # 生成列表
    result = list(range(start, end))
    
    return result

def haversine_distance(lat1, lon1, lat2, lon2):
    # 将经纬度从度数转换为弧度
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    # 地球半径（平均值），单位为千米
    radius = 6371.0

    # Haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # 计算距离
    distance = radius * c

    return distance



for t in [0,1,2]:
    
    if t==0:
        df = pd.read_csv("../外部資料集/Training Dataset.csv")
    elif t==1:
        df = pd.read_csv("../外部資料集/Public Dataset.csv")
    else:
        df = pd.read_csv("../外部資料集/Private Dataset.csv")
    
    external_df =  pd.read_csv("../外部資料集/實價登錄資料.csv")
    #external_df = external_df[external_df.lat.notna()]    
    external_df.loc[external_df["預售屋"] == True, "屋齡"] = 0

    
    
    #external_df = external_df[(~external_df['移轉層次'].str.contains('，|一層', na=False)) & (external_df["預售屋"]!=True)]
    external_df = external_df[~external_df['移轉層次'].str.contains('一層', na=False)]
        
    
        
    a = external_df[(external_df["建物型態"]=="公寓(5樓含以下無電梯)")] 
    b = external_df[(external_df["建物型態"]=="住宅大樓(11層含以上有電梯)")] 
    c = external_df[(external_df["建物型態"]=="透天厝")] 
    d = external_df[(external_df["建物型態"]=="華廈(10層含以下有電梯)")] 

    
    bar = tqdm(df.iterrows(), total=len(df))
    
    for idx,row in bar:
        lng = row["lng"]
        lat = row["lat"]
        road = row["路名"]
        stair = row["移轉層次"]
        
        floor_list = generate_integer_list(int(stair))
        floor_list = [number_to_chinese(f)+"層" for f in floor_list]
        #print(stair,floor_list)
        pattern = '|'.join(floor_list)
        
        
        if row["建物型態"]=="公寓(5樓含以下無電梯)":
            part_of_external_df=a
        elif row["建物型態"]=="住宅大樓(11層含以上有電梯)":
            part_of_external_df=b
        elif row["建物型態"]=="透天厝":
            part_of_external_df=c
        elif row["建物型態"]=="華廈(10層含以下有電梯)":
            part_of_external_df=d
            
        
        part_of_external_df = part_of_external_df[(part_of_external_df['地址'].str.contains(road, na=False))&\
                                                  (part_of_external_df["鄉鎮市區"]==row["鄉鎮市區"])]
        
        part_of_external_df = part_of_external_df[part_of_external_df['移轉層次'].apply(lambda x: any(floor in str(x).split(',') for floor in floor_list))]

        

        if len(part_of_external_df)>0:
            
            for y in [1,3,5]:
                    
                df_ = part_of_external_df[abs(part_of_external_df["屋齡"]-row["屋齡"])<=y]
                count = len(df_)
               
                if count>0:
                    
                    avg_price = df_[["單價元平方公尺"]].mean().item()
                    max_price = df_[["單價元平方公尺"]].max().item()
                    min_price = df_[["單價元平方公尺"]].min().item()
                    median_price = df_[["單價元平方公尺"]].median().item()
                    std_price =  df_[["單價元平方公尺"]].std().item()
                    
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，平均單價"] = avg_price
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，最大單價"] = max_price
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，最小單價"] = min_price
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，單價中位數"] = median_price
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，交易次數"] = count
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，單價標準差"] = std_price
                    
                else:
                    df.loc[idx, f"相同路段，屋齡差小於{y}年，交易次數"] = 0
        
    
   
    if t==0:
        df.to_csv("../外部資料集/Training Dataset.csv",index=False)
    elif t==1:
        df.to_csv("../外部資料集/Public Dataset.csv",index=False)
    else:
        df.to_csv("../外部資料集/Private Dataset.csv",index=False)            

        
    print("=="*20)

    
    

