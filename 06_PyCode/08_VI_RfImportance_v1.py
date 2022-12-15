# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:39:26 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""
import pandas as pd
import numpy as np

from joblib import load

def runLocallyOrRemotely(Locally_Or_Remotely):
    locally_or_remotely = Locally_Or_Remotely
    if locally_or_remotely == 'y':
        repo_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
        repo_figure_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/04_Figure/"
    elif locally_or_remotely == 'n':
        repo_location = "/home/usr6/q70176a/DP15/"
        repo_result_location = "/home/usr6/q70176a/DP15/03_Results/"
        repo_figure_location = "/home/usr6/q70176a/DP15/04_Figure/"
    elif locally_or_remotely == 'wsl':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
        repo_figure_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/04_Figure/"
    return repo_location, repo_result_location, repo_figure_location



REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely(Locally_Or_Remotely = "y")

RF_IMPORTANCE_LSOVERALL = load(REPO_RESULT_LOCATION + "98_LSoverall_RfImportance.joblib")
