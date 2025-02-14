# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 19:26:36 2023

@author: FST
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
###金融機構基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/金融機構基本資料.csv')
df1 = df[df["金融機構名稱"].str.contains("農會")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/農會.csv",index=False)

df1 = df[df["金融機構名稱"].str.contains("漁會")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/漁會.csv",index=False)

df1 = df[~df["金融機構名稱"].str.contains("農會|漁會")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/銀行.csv",index=False)
unique = df1["金融機構名稱"].unique()

###醫療機構基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/醫療機構基本資料.csv')

df1 = df[df["型態別"].str.contains("診所")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/診所.csv",index=False)

df1 = df[df["型態別"].str.contains("醫院")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/醫院.csv",index=False)

df1 = df[df["型態別"].str.contains("牙醫")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/牙醫.csv",index=False)

df1 = df[df["型態別"].str.contains("中醫")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/中醫.csv",index=False)

df1 = df[df["型態別"].str.contains("西醫")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/西醫.csv",index=False)

###捷運站點資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/捷運站點資料.csv')
df['站點UID'] = df['站點UID'].str.split('-').str[0]
unique = df["站點UID"].unique()
for i in unique:
    unique_df = df[df["站點UID"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/捷運_{i}線.csv",index=False)


###國中基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/國中基本資料.csv')

df1 = df[~df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立國中.csv",index=False)

df1 = df[df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/公立國中.csv",index=False)

###國小基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/國小基本資料.csv')

df1 = df[~df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立國小.csv",index=False)

df1 = df[df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/公立國小.csv",index=False)

###高中基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/高中基本資料.csv')

df1 = df[~df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/高職.csv",index=False)

df1 = df[df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/高中.csv",index=False)

df1 = df[~df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立高中職.csv",index=False)

df1 = df[~df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1 = df1[~df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立高職.csv",index=False)

df1 = df[~df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1 = df1[df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立高中.csv",index=False)

df1 = df[df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/公立高中職.csv",index=False)

df1 = df[df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1 = df1[~df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/公立高職.csv",index=False)

df1 = df[df["學校名稱"].str.contains('國立|市立|縣立')].reset_index()
df1 = df1[df["學校名稱"].str.contains('中')].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/公立高中.csv",index=False)


###大學基本資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/大學基本資料.csv')
unique = df["體系別"].unique()
for i in unique:
    unique_df = df[df["體系別"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/{i.split(' ')[1]}大學.csv",index=False)
    
df1 = df[df["學校名稱"].str.contains("國立")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/國立大學.csv",index=False)
unique = df1["體系別"].unique()
for i in unique:
    unique_df = df1[df1["體系別"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/國立{i.split(' ')[1]}大學.csv",index=False)

df1 = df[~df["學校名稱"].str.contains("國立")].reset_index()
df1.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立大學.csv",index=False)
unique = df1["體系別"].unique()
for i in unique:
    unique_df = df1[df1["體系別"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/私立{i.split(' ')[1]}大學.csv",index=False)

###便利商店
df = pd.read_csv(f'../外部資料集/外部輔助資料集/便利商店.csv')
unique = df["公司名稱"].unique()
for i in unique:
    unique_df = df[df["公司名稱"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/{i}.csv",index=False)


###火車站點資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/火車站點資料.csv')
unique = df["車站級別"].unique()
name_list = ["特等站","一等站","二等站","三等站","簡易站","招呼站"]
for i in unique:
    unique_df = df[df["車站級別"]==i].reset_index()
    name = name_list[i]
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/火車站_{name}.csv",index=False)
    

###ATM資料
df = pd.read_csv(f'../外部資料集/外部輔助資料集/ATM資料.csv')
unique = df["裝設金融機構名稱"].unique()

for i in unique:
    unique_df = df[df["裝設金融機構名稱"]==i].reset_index()
    unique_df.to_csv(f"../外部資料集/拆分後的外部輔助資料集/{i}_ATM.csv",index=False)
