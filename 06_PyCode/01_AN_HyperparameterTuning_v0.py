# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 14:26:09 2022

@author: chaol
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from sklearn.model_selection import train_test_split

### X and y
def getXandY(Output_Vari):
    y = pd.read_csv(REPO_LOCATION + "01_Data/10_y_" + Output_Vari + "_29IndVar.csv", index_col=0)
    y = y.iloc[:,0].to_numpy()
    X = pd.read_csv(REPO_LOCATION + "01_Data/09_X_" + Output_Vari + "_29IndVar.csv", index_col=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, 
                                                        random_state=1)
    return X_train, X_test, y_train, y_test

def findBestParameter(Max_Features, 
                      X_train, X_test, y_train, y_test):    
    base_estimator = RandomForestRegressor(n_estimators=1000, random_state=1,
                                           n_jobs = 6, oob_score = True,
                                           max_features = Max_Features) 
    base_estimator.fit(X_train, y_train)
    oob_score = base_estimator.oob_score_
    test_score = base_estimator.score(X_test, y_test)
    return [Max_Features, oob_score, test_score]

def createLog(Log_Or_Not):
    if Log_Or_Not == "YES":
        file = open(REPO_RESULT_LOCATION + LOG_NAME, "w")
        file.write("go!\n")
        file.write(str(datetime.now()) + "\n")
        file.close()
    return None

def run(Output_Of_Interest):
    X_train, X_test, y_train, y_test = getXandY(Output_Of_Interest)
    for Max_Features in list(range(1, 28)):
        record = findBestParameter(Max_Features,
                                   X_train, X_test,
                                   y_train, y_test)
        file = open(REPO_RESULT_LOCATION + LOG_NAME, "a")
        file.write(str(record) + "\n")
        file.write(str(datetime.now()) + "\n")
        file.close()
    addRecordToLog(Output_Of_Interest)
    return None

def addRecordToLog(Input_Element):
    now_time = datetime.now()
    f = open(REPO_RESULT_LOCATION + LOG_NAME, "a")
    f.write(str(Input_Element) + " ; ")
    f.write(str(now_time) + "\n")
    f.close()
    return None

REPO_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
REPO_RESULT_LOCATION = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
LOG_NAME = "01_TuningLog.txt"

createLog("YES")

run("LSoverall")
run("Happinessoverall")
run("LSrelative")
run("Happinessrelative")


"""
mat = search.cv_results_
check_table = pd.DataFrame(np.array(
    [mat["rank_test_score"], mat['param_max_features'],
     mat['param_min_samples_split'], mat['mean_test_score'],
     mat['std_test_score']
     ]).T)

param_grid= {'max_features': [1, 2, 3],
             'min_samples_split':[2, 5, 10, 15, 20, 25, 30, 35, 40]
             }
base_estimator = RandomForestRegressor(oob_score=True, random_state=1,
                                       n_estimators = 100, n_jobs=-1)
search100 = GridSearchCV(base_estimator, param_grid, n_jobs=1, cv=10,
                      verbose=50, scoring='r2')
search100.fit(X, y)
search100.best_estimator_
mat = search100.cv_results_
check_table = pd.DataFrame(np.array(
    [mat["rank_test_score"], mat['param_max_features'],
     mat['param_min_samples_split'], mat['mean_test_score'],
     mat['std_test_score']
     ]).T)
"""