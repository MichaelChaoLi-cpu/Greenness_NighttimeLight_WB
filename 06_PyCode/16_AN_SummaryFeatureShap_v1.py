# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:05:13 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

from glob import glob
from joblib import load
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def runLocallyOrRemotely(Locally_Or_Remotely):
    locally_or_remotely = Locally_Or_Remotely
    if locally_or_remotely == 'y':
        repo_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    elif locally_or_remotely == 'n':
        repo_location = "/home/usr6/q70176a/DP15/"
        repo_result_location = "/home/usr6/q70176a/DP15/07_PyResults/"
    elif locally_or_remotely == 'wsl':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    elif  locally_or_remotely == 'linux':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    elif locally_or_remotely == 'mac':
        repo_location = "/Users/lichao/Library/CloudStorage/OneDrive-KyushuUniversity/15_Article/03_RStudio/"
        repo_result_location = "/Users/lichao/Library/CloudStorage/OneDrive-KyushuUniversity/02_Article/15_RStudio/07_PyResults/"
    repo_figure_location = repo_location + "04_Figure/"
    return repo_location, repo_result_location, repo_figure_location

def summaryFeatureShapReal(Variable_Of_Interest, Output_Variable):
    dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_" + Output_Variable + ".csv", 
                            index_col = 0)
    print(dataframe[Variable_Of_Interest+'_shap'].describe())
    X = dataframe[[Variable_Of_Interest]]
    y = dataframe[Variable_Of_Interest + "_shap"].to_numpy()
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)
    print(f"coefficient: {reg.coef_[0]:.7f}, intercept: {reg.intercept_:.7f}")
    print(r2_score(y, y_pred))
    predictions = reg.predict(X)
    newX = X
    newX['Constant'] = 1
    MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))
    var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
    sd_b = np.sqrt(var_b) 
    t_coef = reg.coef_[0]/sd_b[0]
    t_interc = reg.intercept_/sd_b[1]
    print(f"T coefficient: {t_coef:.3f}, T intercept: {t_interc:.3f}")
    return None

def checkLocalModelAccuracy(Variable_Of_Interest, Output_Variable):
    file_list = glob(REPO_RESULT_LOCATION +  "*" + Variable_Of_Interest + "_spatialcoefficient_" + Output_Variable +".joblib")
    spatial_coefficient = load(file_list[0])
    dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_" + Output_Variable + ".csv", index_col = 0)
    dataframe.reset_index(inplace=True)
    y_pred = dataframe[Variable_Of_Interest] * spatial_coefficient[Variable_Of_Interest+'_coef'] + spatial_coefficient[Variable_Of_Interest+'_interc']
    y = dataframe[Variable_Of_Interest + '_shap']
    return r2_score(y.to_numpy(), y_pred.to_numpy())
    

REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')
summaryFeatureShapReal('NDVI', 'LSoverall')
summaryFeatureShapReal('NDVI', 'LSrelative')
summaryFeatureShapReal('NDVI', 'Happinessoverall')
summaryFeatureShapReal('NDVI', 'Happinessrelative')

summaryFeatureShapReal('NTL', 'LSoverall')
summaryFeatureShapReal('NTL', 'LSrelative')
summaryFeatureShapReal('NTL', 'Happinessoverall')
summaryFeatureShapReal('NTL', 'Happinessrelative')

checkLocalModelAccuracy('NDVI', 'LSoverall')
checkLocalModelAccuracy('NDVI', 'LSrelative')
checkLocalModelAccuracy('NDVI', 'Happinessoverall')
checkLocalModelAccuracy('NDVI', 'Happinessrelative')

checkLocalModelAccuracy('NTL', 'LSoverall')
checkLocalModelAccuracy('NTL', 'LSrelative')
checkLocalModelAccuracy('NTL', 'Happinessoverall')
checkLocalModelAccuracy('NTL', 'Happinessrelative')
