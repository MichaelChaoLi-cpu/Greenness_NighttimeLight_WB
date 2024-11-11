# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 15:41:29 2023

@author: chaol

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
    
for WSL
"""

from glob import glob 
from math import sqrt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score

def runLocallyOrRemotely(locally_or_remotely):
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

def makeModel(Variable_Of_Interest):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    y_file_name = glob(REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv")
    y = pd.read_csv(y_file_name[0], index_col=0).to_numpy()
    
    model = RandomForestRegressor(n_estimators=1000, min_samples_split = 100, 
                                  max_features = 7, random_state=1, oob_score=True,
                                  n_jobs=-1)
    model.fit(X, y) 
    return model, X, y

def getStatisticalIndicator(Variable_Of_Interest):
    model, X, y = makeModel(Variable_Of_Interest)
    y_pred = model.predict(X)
    rf_list = [r2_score(y, y_pred), sqrt(mean_squared_error(y, y_pred)), mean_absolute_error(y, y_pred), model.oob_score_]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    model = LinearRegression()
    scores = cross_val_score(model, X, y, cv=10)
    lm_list = [r2_score(y, y_pred), sqrt(mean_squared_error(y, y_pred)), mean_absolute_error(y, y_pred), scores.mean()]
    return [rf_list, lm_list]

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('wsl')
OVLS_list = getStatisticalIndicator("LSoverall")

RLS_list = getStatisticalIndicator("LSrelative")

OH_list = getStatisticalIndicator("Happinessoverall")

RH_list = getStatisticalIndicator("Happinessrelative")

Statistical_Indicator_Df = pd.concat([pd.DataFrame(OVLS_list), pd.DataFrame(RLS_list), 
                                      pd.DataFrame(OH_list), pd.DataFrame(RH_list)])

Statistical_Indicator_Df.columns = ['R2', 'RMSE', 'MAE', 'CV score']
Statistical_Indicator_Df.to_csv(REPO_RESULT_LOCATION + "97_Statistical_Indicator_Df.csv")


