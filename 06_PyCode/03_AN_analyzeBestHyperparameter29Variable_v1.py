# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:01:17 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
    
"""

from joblib import load
import pandas as pd
import numpy as np

def runLocallyOrRemotely():
    locally_or_remotely = input("Run the code locally? [y/n/wsl]:")
    if locally_or_remotely == 'y':
        repo_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    else if locally_or_remotely == 'n':
        repo_location = "/home/usr6/q70176a/DP15/"
        repo_result_location = "/home/usr6/q70176a/DP15/03_Results/"
    else if locally_or_remotely == 'wsl':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
    return repo_location, repo_result_location

def makeHyperparameterTable(Grid_Search_File_Name):
    grid_search_cv = load(REPO_RESULT_LOCATION + Grid_Search_File_Name)
    cv_result = grid_search_cv.cv_results_
    check_table = pd.DataFrame(np.array(
        [cv_result["rank_test_score"], cv_result['param_max_features'],
         cv_result['param_min_samples_split'], cv_result['mean_test_score'],
         cv_result['std_test_score']
         ]).T)
    check_table.columns = ["rank_test_score", 'param_max_features',
                           'param_min_samples_split', 'mean_test_score', 
                           'std_test_score']
    return check_table



REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely()
Ls_Overall_Check_Table = makeHyperparameterTable("01_hyperTuningLsOverall.joblib")
Happiness_Overall_Check_Table = makeHyperparameterTable("02_hyperTuningHappinessOverall.joblib")
Ls_Relative_Check_Table = makeHyperparameterTable("03_hyperTuningLsRelative.joblib")
Happiness_Relative_Check_Table = makeHyperparameterTable("04_hyperTuningHappinessRelative.joblib")

"""
Ls_Overall_Check_Table: max_features - 7; min_samples_split - 100;
Happiness_Overall_Check_Table: max_features - 7; min_samples_split - 100;
Ls_Relative_Check_Table: max_features - 8; min_samples_split - 100;
Happiness_Relative_Check_Table: max_features - 6; min_samples_split - 100;
"""


