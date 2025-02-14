# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 10:58:29 2023

@author: FST
"""
import pandas as pd
from tqdm import tqdm
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")


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
    
    for external_data in os.listdir("../外部資料集/外部輔助資料集"):
        if ".csv" in external_data:
            external_df = pd.read_csv(f'../外部資料集/外部輔助資料集/{external_data}')
            if "基本資料" in external_data:  
                feature_name = external_data.split("基本資料")[0]
            elif "資料" in external_data:  
                feature_name = external_data.split("資料")[0]
            else:
                feature_name = external_data.split(".")[0]
            
            if feature_name=="高中":
                feature_name="高中職"
                
            external_df = external_df.drop_duplicates(subset=['lat', 'lng'])
            target_coords = external_df[['lat', 'lng']].values
           
            print(feature_name)
            bar = tqdm(df.iterrows(), total=len(df))
            for idx,row in bar:
                lng = row["lng"]
                lat = row["lat"]
            
                distances = haversine_distance(lat, lng, target_coords[:, 0], target_coords[:, 1])
                for i in [1,3,5,7,9]:
                    count = len(np.where(distances<i)[0])
                    df.loc[idx, f"距離{feature_name}小於{i}公里"] = count
                    #df.loc[idx, f"{i}公里內，{feature_name}數量"] = count
                    
    if t==0:
        df.to_csv("../外部資料集/Training Dataset.csv",index=False)
    elif t==1:
        df.to_csv("../外部資料集/Public Dataset.csv",index=False)
    else:
        df.to_csv("../外部資料集/Private Dataset.csv",index=False)        
    print("=="*20)
    
    
