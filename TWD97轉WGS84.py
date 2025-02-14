# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 08:48:24 2023

@author: FST
"""
import pandas as pd
import pyproj
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def TWD2WGS(twd97_x_list,twd97_y_list):
    twd97 = pyproj.Proj(init='epsg:3826')  # TWD97 的 EPSG 代码
    wgs84 = pyproj.Proj(init='epsg:4326')  # WGS84 的 EPSG 代码
    if len(twd97_x_list)!=len(twd97_y_list):
        print("Error")
        return [],[]
    
    lat=[]
    lng=[]
    bar = tqdm(range(len(twd97_x_list)), total=len(twd97_x_list))
    for i in bar:
        twd97_x = twd97_x_list[i]
        twd97_y = twd97_y_list[i]
        longitude, latitude = pyproj.transform(twd97, wgs84, twd97_x, twd97_y)
        lng.append(longitude)
        lat.append(latitude)
    
    return lng,lat

for t in [0,1,2]:
    
    if t==0:
        df = pd.read_csv("../外部資料集/Training Dataset.csv")
    elif t==1:
        df = pd.read_csv("../外部資料集/Public Dataset.csv")
    else:
        df = pd.read_csv("../外部資料集/Private Dataset.csv")
        
    
    twd97_x_list = list(df["橫坐標"])
    twd97_y_list = list(df["縱坐標"])
    lng,lat = TWD2WGS(twd97_x_list,twd97_y_list)
    df["lat"]=lat
    df["lng"]=lng
    
    if t==0:
        df.to_csv("../外部資料集/Training Dataset.csv",index=False)
    elif t==1:
        df.to_csv("../外部資料集/Public Dataset.csv",index=False)
    else:
        df.to_csv("../外部資料集/Private Dataset.csv",index=False) 
    
