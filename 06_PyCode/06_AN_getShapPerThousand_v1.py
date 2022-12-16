# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:32:22 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import pandas as pd
import numpy as np

from cuml.ensemble import RandomForestRegressor as cuRandomForestRegressor
import cudf
import cupy as cp

from cuml.explainer import KernelExplainer
from joblib import dump, load

import sys

from glob import glob

def getShapCSV(Cu_Explainer, Variable_Of_Interest, kID=1):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    cu_shap_value_merge = Cu_Explainer.shap_values(X.iloc[(kID-1)*1000:kID*1000,:])
    pd.DataFrame(cu_shap_value_merge).to_csv(REPO_RESULT_LOCATION + "shap_thousand_" + str(kID) + ".csv")
    return None

INPUT_PARAMETER_1 = sys.argv[1]
INPUT_PARAMETER_2 = sys.argv[2]

REPO_LOCATION = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
REPO_RESULT_LOCATION = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"

CU_EXPLAINER = load(REPO_RESULT_LOCATION + "99_" + INPUT_PARAMETER_2 + "_cu_explainer.joblib")

getShapCSV(CU_EXPLAINER, INPUT_PARAMETER_2, kID=int(INPUT_PARAMETER_1))
