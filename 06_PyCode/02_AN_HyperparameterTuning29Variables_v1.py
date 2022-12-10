# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 14:17:01 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
    
#!/bin/bash
#PJM -L "rscunit=ito-a"
#PJM -L "rscgrp=ito-m-dbg"
#PJM -L "vnode=16"
#PJM -L "vnode-core=36"
#PJM -L "elapse=01:00:00"
#PJM -j
#PJM -X

module use /home/exp/modulefiles
module load gcc/10.2.0
mpirun  -np 320 -ppn 20 -machinefile ${PJM_O_NODEINF}  -launcher-exec /bin/pjrsh python /home/usr6/q70176a/DP15/06_PyCode/02_AN_HyperparameterTuning29Variables_v1.py


"""

import os
import dask_mpi as dm
from dask.distributed import Client, progress
from dask.distributed import performance_report

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from joblib import dump
import joblib
from dask_ml.model_selection import GridSearchCV

REPO_LOCATION = "/home/usr6/q70176a/DP15/"
REPO_RESULT_LOCATION = "/home/usr6/q70176a/DP15/03_Results/"

dm.initialize(local_directory=os.getcwd(), nthreads = 1, memory_limit = 0.05)
CLIENT = Client()

def tuneHyperparameterLsOverall():
    y = pd.read_csv(REPO_LOCATION + "01_Data/10_y_LSoverall_29IndVar.csv", index_col=0)
    y = y['0'].to_numpy()
    X = pd.read_csv(REPO_LOCATION + "01_Data/09_X_LSoverall_29IndVar.csv", index_col=0)
    param_grid= {'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                  21, 22, 23, 24, 25, 26, 27, 28, 29],
                 'min_samples_split':[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
                 }
    base_estimator = RandomForestRegressor(oob_score=True, n_estimators=1000,
                                           random_state=1)
    search = GridSearchCV(base_estimator, param_grid, cv=10, n_jobs = -1)
    with performance_report(filename = REPO_RESULT_LOCATION + "01_DaskTuningLsOverall.html"):
        search.fit(X, y)
    dump(search, REPO_RESULT_LOCATION + '01_hyperTuningLsOverall.joblib')
    return None

def tuneHyperparameterHappinessOverall():
    y = pd.read_csv(REPO_LOCATION + "01_Data/12_y_Happinessoverall.csv", index_col=0)
    y = y['0'].to_numpy()
    X = pd.read_csv(REPO_LOCATION + "01_Data/11_X_Happinessoverall_29IndVar.csv", index_col=0)
    param_grid= {'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                  21, 22, 23, 24, 25, 26, 27, 28, 29],
                 'min_samples_split':[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
                 }
    base_estimator = RandomForestRegressor(oob_score=True, n_estimators=1000,
                                           random_state=1)
    search = GridSearchCV(base_estimator, param_grid, cv=10, n_jobs = -1)
    with performance_report(filename = REPO_RESULT_LOCATION + "02_DaskTuningHappinessOverall.html"):
        search.fit(X, y)
    dump(search, REPO_RESULT_LOCATION + '02_hyperTuningHappinessOverall.joblib')
    return None

def tuneHyperparameterLsRelative():
    y = pd.read_csv(REPO_LOCATION + "01_Data/14_y_LSrelative_29IndVar.csv", index_col=0)
    y = y['0'].to_numpy()
    X = pd.read_csv(REPO_LOCATION + "01_Data/13_X_LSrelative_29IndVar.csv", index_col=0)
    param_grid= {'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                  21, 22, 23, 24, 25, 26, 27, 28, 29],
                 'min_samples_split':[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
                 }
    base_estimator = RandomForestRegressor(oob_score=True, n_estimators=1000,
                                           random_state=1)
    search = GridSearchCV(base_estimator, param_grid, cv=10, n_jobs = -1)
    with performance_report(filename = REPO_RESULT_LOCATION + "03_DaskTuningLsRelative.html"):
        search.fit(X, y)
    dump(search, REPO_RESULT_LOCATION + '03_hyperTuningLsRelative.joblib')
    return None

def tuneHyperparameterHappinessRelative():
    y = pd.read_csv(REPO_LOCATION + "01_Data/16_y_Happinessrelative.csv", index_col=0)
    y = y['0'].to_numpy()
    X = pd.read_csv(REPO_LOCATION + "01_Data/15_X_Happinessrelative_29IndVar.csv", index_col=0)
    param_grid= {'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                  11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                  21, 22, 23, 24, 25, 26, 27, 28, 29],
                 'min_samples_split':[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
                 }
    base_estimator = RandomForestRegressor(oob_score=True, n_estimators=1000,
                                           random_state=1)
    search = GridSearchCV(base_estimator, param_grid, cv=10, n_jobs = -1)
    with performance_report(filename = REPO_RESULT_LOCATION + "04_DaskTuningHappinessRelative.html"):
        search.fit(X, y)
    dump(search, REPO_RESULT_LOCATION + '04_hyperTuningHappinessRelative.joblib')
    return None

tuneHyperparameterLsOverall()
tuneHyperparameterHappinessOverall()
tuneHyperparameterLsRelative()
tuneHyperparameterHappinessRelative()

CLIENT.close()

"""
REPO_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
REPO_RESULT_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"


"""
