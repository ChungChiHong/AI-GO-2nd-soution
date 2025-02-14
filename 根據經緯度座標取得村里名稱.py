# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 19:53:47 2023

@author: foresight
"""
import pandas as pd
from tqdm import tqdm
import re
import requests
import warnings
warnings.filterwarnings("ignore")


training_df = pd.read_csv('../外部資料集/Training Dataset.csv')
public_df = pd.read_csv('../外部資料集/Public Dataset.csv')
private_df = pd.read_csv('../外部資料集/Private Dataset.csv')

pattern = r'<villageName>(.*?)</villageName>'
village_names = []
for t in [0,1,2]:
    
    if t==0:
        df = pd.read_csv("../外部資料集/Training Dataset.csv")
    elif t==1:
        df = pd.read_csv("../外部資料集/Public Dataset.csv")
    else:
        df = pd.read_csv("../外部資料集/Private Dataset.csv")
       
    bar = tqdm(df.iterrows(), total=len(df))
    for idx,row in bar:
       lng = row["lng"]
       lat = row["lat"]
       
       # call 單點坐標回傳行政區(戶政) API
       url = f"https://api.nlsc.gov.tw/other/TownVillagePointQuery1/{lng}/{lat}/4326"
       response = requests.get(url)

       match = re.search(pattern, response.text, re.DOTALL)
       if match:
           village_name = match.group(1)
           village_names.append(village_name)
       else:
           village_names.append(None)

    df["村里"]=village_names

    if t==0:
        df.to_csv("../外部資料集/Training Dataset.csv",index=False)
    elif t==1:
        df.to_csv("../外部資料集/Public Dataset.csv",index=False)
    else:
        df.to_csv("../外部資料集/Private Dataset.csv",index=False) 