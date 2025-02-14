# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 19:38:21 2023

@author: FST
"""

import pandas as pd
from tqdm import tqdm
import geocoder


lat = []
lng = []

df = pd.read_csv('../外部資料集/實價登錄資料.csv')
bar = tqdm(df.iterrows(),total=len(df))
for idx,row in bar:
    address = row["地址"]
   
    
    g = geocoder.arcgis(address)
    if len(g)!=0:
        lat.append(g.json['lat'])
        lng.append(g.json['lng']) 

    else:
        lat.append(None)
        lng.append(None) 

    #print(g.json['lat'],g.json['lng'])
df["lat"] = lat
df["lng"] = lng

df.to_csv('../外部資料集/實價登錄資料.csv',index=False)



    