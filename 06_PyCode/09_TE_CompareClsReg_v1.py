# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:36:49 2023

@author: chaol

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
    
"""

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def runLocallyOrRemotely():
    locally_or_remotely = input("Run the code locally? [y/n/wsl]:")
    if locally_or_remotely == 'y':
        repo_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    elif locally_or_remotely == 'n':
        repo_location = "/home/usr6/q70176a/DP15/"
        repo_result_location = "/home/usr6/q70176a/DP15/03_Results/"
    elif locally_or_remotely == 'wsl':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    return repo_location, repo_result_location

# update 2023.1.30
def getXandY(Output_Vari):
    y = pd.read_csv(REPO_LOCATION + "01_Data/10_y_" + Output_Vari + "_29IndVar.csv", index_col=0)
    y = y.iloc[:,0].to_numpy().astype('int')
    X = pd.read_csv(REPO_LOCATION + "01_Data/09_X_" + Output_Vari + "_29IndVar.csv", index_col=0)
    return X, y

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely()
X, y = getXandY("LSoverall")


model_cls = RandomForestRegressor(n_estimators=1000, random_state=1,
                                  n_jobs = -1, oob_score = True) 
model_cls.fit(X, y)
print(model_cls.oob_score_)

model_reg = RandomForestRegressor(n_estimators=1000, random_state=1,
                                  n_jobs = -1, oob_score = True) 
model_reg.fit(X, y)
print(model_reg.oob_score_)

"""
This script is to confirm whether cls is better than reg.
RESULT reg is better
"""