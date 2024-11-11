# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:01:20 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import os

import pandas as pd
import numpy as np

from glob import  glob
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor

import matplotlib.pyplot as plt

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
    return repo_location, repo_result_location

def makeFolder(FolderName):
    if not os.path.exists(REPO_FIGURE_LOCATION + FolderName):
        os.makedirs(REPO_FIGURE_LOCATION + FolderName)
    return REPO_FIGURE_LOCATION + FolderName + "/"
    
def plotScatterColoredByOther(Variable_Of_Interest, y_Lim, Output_Variable):
    dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_" + Output_Variable + ".csv", 
                            index_col = 0)
    temp_folder = makeFolder(Output_Variable + '_' + Variable_Of_Interest)
    feature_list = dataframe.columns.tolist()[:30]
    feature_list.remove(Variable_Of_Interest)
    for feature in feature_list:
        p1 = plt.scatter(dataframe[Variable_Of_Interest], dataframe[Variable_Of_Interest + "_shap"], 
                         c = dataframe[feature], 
                         alpha=0.2, marker='.', edgecolors='none')
        plt.ylim(-y_Lim, y_Lim)
        clb = plt.colorbar(p1, label=feature)
        plt.xlabel(Variable_Of_Interest)
        plt.ylabel(Variable_Of_Interest + " SHAP")
        plt.savefig(temp_folder + Variable_Of_Interest + "_" + feature + ".jpg",
                    dpi = 300, bbox_inches='tight')
        plt.show()
    return None


REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')
REPO_FIGURE_LOCATION = REPO_LOCATION + "04_Figure/"


plotScatterColoredByOther("NDVI", 0.1, 'LSoverall')
plotScatterColoredByOther("NTL", 0.2, 'LSoverall')

plotScatterColoredByOther("NDVI", 0.1, 'LSrelative')
plotScatterColoredByOther("NTL", 0.2, 'LSrelative')

plotScatterColoredByOther("NDVI", 0.1, 'Happinessoverall')
plotScatterColoredByOther("NTL", 0.2, 'Happinessoverall')

plotScatterColoredByOther("NDVI", 0.1, 'Happinessrelative')
plotScatterColoredByOther("NTL", 0.2, 'Happinessrelative')








"""

dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_LSoverall.csv", 
                        index_col = 0)
def printR2(dataframe):
    X = dataframe[['NDVI']]
    y = dataframe['NDVI_shap']
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    print(r2_score(y, y_pred))
    
    X = dataframe[['NTL']]
    y = dataframe['NTL_shap']
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    print(r2_score(y, y_pred))
    return None

dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_LSoverall.csv", 
                        index_col = 0)
printR2(dataframe)

dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_LSrelative.csv", 
                        index_col = 0)
printR2(dataframe)

dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_Happinessoverall.csv", 
                        index_col = 0)
printR2(dataframe)

dataframe = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_Happinessrelative.csv", 
                        index_col = 0)
printR2(dataframe)
"""
