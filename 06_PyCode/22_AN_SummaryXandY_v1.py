# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:29:04 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

from glob import glob
import numpy as np
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
    return repo_location, repo_result_location

def getTotalDataset():
    y_ovls = pd.read_csv(REPO_LOCATION + "01_Data/10_y_LSoverall_29IndVar.csv", index_col=0)
    y_rls = pd.read_csv(REPO_LOCATION + "01_Data/12_y_Happinessoverall.csv", index_col=0)
    y_oh = pd.read_csv(REPO_LOCATION + "01_Data/14_y_LSrelative_29IndVar.csv", index_col=0)
    y_rh = pd.read_csv(REPO_LOCATION + "01_Data/16_y_Happinessrelative.csv", index_col=0)
    X = pd.read_csv(REPO_LOCATION + "01_Data/09_X_LSoverall_29IndVar.csv", index_col=0)
    dataframe = pd.concat([y_ovls, y_rls, y_oh, y_rh, X], axis=1)
    dataframe_describe = dataframe.describe().T
    dataframe_describe.to_csv(REPO_RESULT_LOCATION + "18_Datasummary.csv")
    return None


REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')
getTotalDataset()






