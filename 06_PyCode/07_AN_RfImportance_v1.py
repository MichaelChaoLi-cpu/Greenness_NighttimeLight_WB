# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 08:35:48 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
   
#!/bin/bash
#PJM -L "rscunit=ito-a"
#PJM -L "rscgrp=ito-m"
#PJM -L "vnode=16"
#PJM -L "vnode-core=36"
#PJM -L "elapse=24:00:00"
#PJM -j
#PJM -X
module use /home/exp/modulefiles
module load gcc/10.2.0
mpirun  -np 80 -ppn 5 -machinefile ${PJM_O_NODEINF}  -launcher-exec /bin/pjrsh python /home/usr6/q70176a/DP15/06_PyCode/07_AN_RfImportance_v1.py
"""

import os
import dask_mpi as dm
from dask.distributed import Client, progress

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from joblib import dump
import joblib

from glob import glob
from datetime import datetime

def runLocallyOrRemotely(Locally_Or_Remotely):
    locally_or_remotely = Locally_Or_Remotely
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

def initializeLogFile(File_Name):
    file_full_name = REPO_RESULT_LOCATION + File_Name
    start_time = datetime.now()
    f = open(file_full_name, "w")
    f.write("Initialized!" + " ; ")
    f.write(str(start_time) + "\n")
    f.close()
    return start_time, file_full_name

def addRecordToLog(Input_Element):
    now_time = datetime.now()
    f = open(FILE_FULL_NAME, "a")
    f.write(str(Input_Element) + " ; ")
    f.write(str(now_time - LOG_START_TIME) + " ; ")
    f.write(str(now_time) + "\n")
    f.close()
    return None

def getXY(Variable_Of_Interest):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    y_file_name = glob(REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv")
    y = pd.read_csv(y_file_name[0], index_col=0)
    y = y.iloc[:,0].to_numpy()
    return X, y

def getModel(X, y, max_features):
    base_estimator = RandomForestRegressor(oob_score=True, n_estimators=1000,
                                           random_state=1, n_jobs=-1, 
                                           min_samples_split = 100, max_features = max_features)
    with joblib.parallel_backend("dask"):
        base_estimator.fit(X, y)
    return base_estimator

def getImportance(model, X, y, Variable_Of_Interest):
    with joblib.parallel_backend("dask"):
        result = permutation_importance(model, X, y, n_repeats=10, 
                                        random_state=1, scoring = "r2")
    dump(result, REPO_RESULT_LOCATION + "98_" + Variable_Of_Interest + "_RfImportance.joblib")
    return None


REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely(Locally_Or_Remotely = "n")

LOG_NAME = "02_RfImportanceLog.txt"
LOG_START_TIME, FILE_FULL_NAME = initializeLogFile(LOG_NAME)

dm.initialize(local_directory=os.getcwd(),  nthreads = 1, memory_limit = 0.2)
CLIENT = Client()
addRecordToLog(CLIENT)

X, y = getXY("LSoverall")
model = getModel(X, y, 7)
getImportance(model, X, y, "LSoverall")
addRecordToLog("LSoverall")

X, y = getXY("Happinessoverall")
model = getModel(X, y, 7)
getImportance(model, X, y, "Happinessoverall")
addRecordToLog("Happinessoverall")

X, y = getXY("LSrelative")
model = getModel(X, y, 7)
getImportance(model, X, y, "LSrelative")
addRecordToLog("LSrelative")

X, y = getXY("Happinessrelative")
model = getModel(X, y, 7)
getImportance(model, X, y, "Happinessrelative")
addRecordToLog("Happinessrelative")

CLIENT.close()

