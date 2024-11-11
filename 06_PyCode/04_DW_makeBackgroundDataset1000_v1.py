# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:33:33 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split 
from glob import glob

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

def makeBackgroundData1000(Variable_Of_Interest):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    y_file_name = glob(REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv")
    y = pd.read_csv(y_file_name[0], index_col=0)
    y = y.iloc[:,0].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1000,
                                                        random_state=1)
    X_test.to_csv(REPO_LOCATION + "01_Data/99_" + Variable_Of_Interest + "_1000_Background.csv")
    return None

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely()
makeBackgroundData1000("LSoverall")
makeBackgroundData1000("LSrelative")
makeBackgroundData1000("Happinessoverall")
makeBackgroundData1000("Happinessrelative")




