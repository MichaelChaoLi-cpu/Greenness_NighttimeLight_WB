# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 09:56:28 2023

@author: chaol

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import pandas as pd
import numpy as np

from glob import  glob

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

def mergeShapDatasetLsoverall():
    csv_read_list = []
    for order_num in list(range(1, 385, 1)):
        csv_name = REPO_RESULT_LOCATION + "shap_thousand_" + str(order_num) + ".csv"
        csv_read = pd.read_csv(csv_name, index_col=0)
        csv_read_list.append(csv_read)
    shap_value_merge = pd.concat(csv_read_list, axis=0)
    shap_value_merge.reset_index(inplace = True)
    shap_value_merge.drop(columns='index', inplace=True)
    return shap_value_merge

def mergeShapDataset(Variable_Of_Interest):
    csv_read_list = []
    for order_num in list(range(1, 385, 1)):
        csv_name = REPO_RESULT_LOCATION + "shap_thousand_" + str(order_num) + "_" + Variable_Of_Interest + ".csv"
        csv_read = pd.read_csv(csv_name, index_col=0)
        csv_read_list.append(csv_read)
    shap_value_merge = pd.concat(csv_read_list, axis=0)
    shap_value_merge.reset_index(inplace = True)
    shap_value_merge.drop(columns='index', inplace=True)
    return shap_value_merge

def getXwithShap(Merged_Shap_Value, Variable_Of_Interest):
    data_location = REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv"
    data_location = glob(data_location)[0]
    X = pd.read_csv(data_location)
    X_colname = X.columns
    shap_colnames = X_colname[1:] + "_shap"
    Merged_Shap_Value.columns = shap_colnames
    data_location = REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv"
    data_location = glob(data_location)[0]
    y = pd.read_csv(data_location)
    y = y.iloc[:,[1]]
    dataset_to_analysis = pd.concat([X, y, Merged_Shap_Value], axis=1)
    return dataset_to_analysis

def run(Variable_Of_Interest):
    REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')
    if Variable_Of_Interest == 'LSoverall':
        Merged_Shap_Value = mergeShapDatasetLsoverall()
    else:
        Merged_Shap_Value = mergeShapDataset(Variable_Of_Interest)
    Dataset_To_Analysis = getXwithShap(Merged_Shap_Value, Variable_Of_Interest)
    Dataset_To_Analysis.to_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_"+ Variable_Of_Interest +".csv", index = False)
    return None

if __name__ == '__main__':
    run('LSoverall')
    run('LSrelative')
    run('Happinessoverall')
    run('happinessrelative')

