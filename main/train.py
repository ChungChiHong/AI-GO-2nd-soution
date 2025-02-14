# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:26:59 2023

@author: foresight
"""

       
import h2o
from h2o.automl import H2OAutoML
#h2o.init()
h2o.init(min_mem_size_GB=8)
#h2o.cluster().shutdown()
#h2o.estimators.xgboost.H2OXGBoostEstimator.available()
import os 
import pandas as pd
import numpy as np


submission_list = os.listdir("./submission/")
submission_id = 0
for submission_name in submission_list:
    if int(submission_name.split(".")[0])>submission_id:
       submission_id=int(submission_name.split("_")[0].split(".")[0])
    
submission_id += 1
print(f"submission id:{submission_id}")


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

    n = 1  # predict n times
    seed = 42
    drop = ['郵局','交易','ID',"相同路段，屋齡大於1~3年，單價標準差","相同路段，屋齡小於1~3年，單價標準差"]

    
if __name__ == "__main__":
    
    set_seed(CFG.seed)   
    Logger = init_logger(log_file=f"./log/{submission_id}.txt")
    with open(f"./log/{submission_id}.txt", 'w') as f:
        for attr in dir(CFG):
            if not callable(getattr(CFG, attr)) and not attr.startswith("__"):
                f.write('{} = {}\n'.format(attr, getattr(CFG, attr)))
                
    train_df = pd.read_csv('../../外部資料集/Training Dataset - final.csv')
    test_df = pd.read_csv('../../外部資料集/Public Dataset - final.csv')

    
  
    
    if CFG.drop:
        columns_to_remove = [col for col in train_df.columns if any(keyword in col for keyword in CFG.drop)]
        train_df = train_df.drop(columns=columns_to_remove)
        test_df = test_df.drop(columns=columns_to_remove)
        
        

      
    test_df = h2o.H2OFrame(test_df)[1:, :]
    

    submission_pred = []
    
    
    for n in range(CFG.n):
        
        Logger.info('--'*20)
        
        X=train_df
        Y=train_df.loc[:,['單價']]
             
        
        X = h2o.H2OFrame(X)[1:, :]
        
        predictors = X.columns
        predictors.remove('單價')

        #train
        model = H2OAutoML(max_runtime_secs=3600, seed=CFG.seed)
        
        model.train(x=predictors, y='單價', training_frame=X)
        
        os.makedirs(f"./model/{submission_id}", exist_ok=True)
        model_path = h2o.save_model(model=model.leader, path=f"../model/{submission_id}/model{submission_id}_n{n}", force=True)
        
        lb=model.leaderboard
        print(lb)

        #inference
        test_pred = model.leader.predict(test_df)
        test_pred = h2o.as_list(test_pred, use_pandas=True)           
        test_pred = test_pred.to_numpy()
        test_pred = np.squeeze(test_pred)

        submission_pred.append(test_pred)
        
        Logger.info(f"Epoch:{n}")
        
        
        submission = pd.read_csv('../../外部資料集/public_submission_template.csv')
        
     
        pred = np.mean(np.array(submission_pred),axis=0)

            
        submission['predicted_price']=pred
        submission.to_csv(f"./submission/public{submission_id}.csv",index=False)


        
    
    
    
    