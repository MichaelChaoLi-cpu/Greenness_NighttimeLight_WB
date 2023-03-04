# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:16:01 2023

@author: chaol

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

from joblib import load
import pandas as pd

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

def convertPandasToCsv(Output_Variable):
    dataframe = load(REPO_RESULT_LOCATION + "08_NDVI_spatialcoefficient_" + Output_Variable + ".joblib")
    dataframe.to_csv(REPO_RESULT_LOCATION + "08_NDVI_spatialcoefficient_" + Output_Variable + ".csv")
    dataframe = load(REPO_RESULT_LOCATION + "09_NTL_spatialcoefficient_" + Output_Variable + ".joblib")
    dataframe.to_csv(REPO_RESULT_LOCATION + "09_NTL_spatialcoefficient_" + Output_Variable + ".csv")
    dataframe = load(REPO_RESULT_LOCATION + "10_income_spatialcoefficient_" + Output_Variable + ".joblib")
    dataframe.to_csv(REPO_RESULT_LOCATION + "10_income_spatialcoefficient_" + Output_Variable + ".csv")
    return None
    


REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('wsl')
convertPandasToCsv("LSoverall")
convertPandasToCsv("LSrelative")
convertPandasToCsv("Happinessoverall")
convertPandasToCsv("Happinessrelative")


