# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:57:45 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
    
for WSL
"""

import pandas as pd
import numpy as np

from cuml.ensemble import RandomForestRegressor as cuRandomForestRegressor
import cudf
import cupy as cp

from cuml.explainer import KernelExplainer
from joblib import dump, load
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

def makeCuModel(Variable_Of_Interest):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    y_file_name = glob(REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv")
    y = pd.read_csv(y_file_name[0], index_col=0)
    cuX = cudf.from_pandas(X)
    cuy = cudf.from_pandas(y)
    
    cumodel = cuRandomForestRegressor(n_estimators=1000, min_samples_split = 100, 
                                      max_features = 7, random_state=1)
    cumodel.fit(cuX, cuy) 
    return cumodel

def makeExplainer(cumodel, Variable_Of_Interest):
    background_dataframe_file_name = glob(REPO_LOCATION + "01_Data/99_" + Variable_Of_Interest + "*.csv")
    background_dataframe = pd.read_csv(background_dataframe_file_name[0],
                                       index_col=0)
    
    cu_explainer = KernelExplainer(model=cumodel.predict,
                                   data=cudf.from_pandas(background_dataframe),
                                   is_gpu_model=True, random_state=1)
    return cu_explainer

def dumpModelAndExplainer(Variable_Of_Interest):
    cumodel = makeCuModel(Variable_Of_Interest)
    cu_explainer = makeExplainer(cumodel, Variable_Of_Interest)
    dump(cumodel, REPO_RESULT_LOCATION + "99_" + Variable_Of_Interest + "_cumodel.joblib")
    dump(cu_explainer, REPO_RESULT_LOCATION + "99_" + Variable_Of_Interest + "_cu_explainer.joblib")
    return None

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely()
dumpModelAndExplainer("LSoverall")
dumpModelAndExplainer("LSrelative")
dumpModelAndExplainer("Happinessoverall")
dumpModelAndExplainer("Happinessrelative")