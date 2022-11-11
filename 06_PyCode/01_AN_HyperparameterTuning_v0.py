# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 14:26:09 2022

@author: chaol
"""

import os
import pyreadr

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from joblib import dump
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import GridSearchCV

REPO_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
REPO_RESULT_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/08_PyResults/"

### X and y
dataset = pyreadr.read_r(REPO_LOCATION  + "01_Data/08_dataset.rf26.rds")
dataset = dataset[None]

X = dataset.iloc[:, 1:27]
y = np.array(dataset.iloc[:, 0:1].values.flatten(), dtype='float64')

param_grid= {'max_features': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                              11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
             'min_samples_split':[2, 5, 10, 15, 20, 25, 30, 35, 40]
             }
base_estimator = RandomForestRegressor(oob_score=True, random_state=1,
                                       n_estimators = 1000, n_jobs=-1)

search = GridSearchCV(base_estimator, param_grid, n_jobs=1, cv=10,
                      verbose=50, scoring='r2')
search.fit(X, y)
search.cv_results_
search.best_estimator_

dump(search, REPO_RESULT_LOCATION + '01_hyperParaSearching.joblib')