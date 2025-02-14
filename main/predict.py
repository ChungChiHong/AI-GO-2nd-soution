# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:40:06 2023

@author: foresight
"""

import h2o
h2o.init()
#h2o.cluster().shutdown()
#h2o.estimators.xgboost.H2OXGBoostEstimator.available()

import os 
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")



def init_logger(log_file):
    from logging import getLogger, INFO, FileHandler, Formatter, StreamHandler
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    handler1 = StreamHandler()
    handler1.setFormatter(Formatter("%(message)s"))
    handler2 = FileHandler(filename=log_file)
    handler2.setFormatter(Formatter("%(message)s"))
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger

def set_seed(seed=42, cudnn_deterministic=True):
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)



class CFG:
    
    n=1
    submission_id=1
    seed = 42
    drop = ['郵局','交易','ID',"相同路段，屋齡大於1~3年，單價標準差","相同路段，屋齡小於1~3年，單價標準差"]
    private = 1

if __name__ == "__main__":
    
    submission_id=CFG.submission_id
    
    set_seed(CFG.seed)   
      
    train_df = pd.read_csv('../../外部資料集/Training Dataset - final.csv')
    if CFG.private:
        test_df = pd.read_csv('../../外部資料集/Private Dataset - final.csv')
    else:
        test_df = pd.read_csv('../../外部資料集/Public Dataset - final.csv')


    if CFG.drop:
        columns_to_remove = [col for col in train_df.columns if any(keyword in col for keyword in CFG.drop)]
        train_df = train_df.drop(columns=columns_to_remove)
        test_df = test_df.drop(columns=columns_to_remove)
        
      
    test_df = h2o.H2OFrame(test_df)[1:, :]
    
    submission_pred = []
    
    
    for n in range(CFG.n):
 
        model_path = f"./model/{submission_id}/model{submission_id}_n{n}"
        model = h2o.load_model(model_path)

        #inference
        test_pred = model.predict(test_df)
        test_pred = h2o.as_list(test_pred, use_pandas=True)           
        test_pred = test_pred.to_numpy()
        test_pred = np.squeeze(test_pred)

        submission_pred.append(test_pred)
            
    
    if CFG.private:
        submission = pd.read_csv('../../外部資料集/private_submission_template.csv')
    else:
        submission = pd.read_csv('../../外部資料集/public_submission_template.csv')
        

    pred = np.mean(np.array(submission_pred),axis=0)
    submission['predicted_price']=pred
    
    if CFG.private:
        submission.to_csv(f"./submission/private{submission_id}.csv",index=False)
    else:
        submission.to_csv(f"./submission/public{submission_id}.csv",index=False)
   
        


        
    
    
    
    