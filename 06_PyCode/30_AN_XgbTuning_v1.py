# -*- coding: utf-8 -*-
"""
Created on Wed May 24 12:56:23 2023

@author: Li Chao
"""

from glob import glob
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import xgboost as xgb

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
    repo_figure_location = repo_location + "04_Figure/"
    return repo_location, repo_result_location, repo_figure_location

### X and y
def getXandY(Output_Vari):
    y_list = glob(REPO_LOCATION + "01_Data/*_y_" + Output_Vari + "*.csv")
    y = pd.read_csv(y_list[0], index_col=0)
    y = y.iloc[:,0].to_numpy() - 1
    X_list = glob(REPO_LOCATION + "01_Data/*_X_" + Output_Vari + "*.csv")
    X = pd.read_csv(X_list[0], index_col=0)
    X = X.drop('NTL', axis=1)
    return X, y

def tuningHyperNestimator(X, y, n_estimators_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for n_estimators in n_estimators_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, learning_rate = 0.01) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {n_estimators}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = n_estimators
    return best_score, best_parameter

def tuningHyperLr(X, y, n_estimators, learning_rate_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in learning_rate_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, learning_rate = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def tuningHyperMaxDepth(X, y, n_estimators, learning_rate,
                        tuning_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in tuning_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, 
                                    learning_rate = learning_rate,
                                    max_depth = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def tuningHyperChild(X, y, n_estimators, learning_rate, max_depth,
                     tuning_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in tuning_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, 
                                    learning_rate = learning_rate,
                                    max_depth = max_depth,
                                    min_child_weight = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def tuningHyperGamma(X, y, n_estimators, learning_rate, max_depth, min_child_weight,
                     tuning_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in tuning_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, 
                                    learning_rate = learning_rate,
                                    max_depth = max_depth,
                                    min_child_weight = min_child_weight,
                                    gamma = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def tuningHyperSubsample(X, y, n_estimators, learning_rate, 
                         max_depth, min_child_weight, gamma,
                         tuning_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in tuning_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, 
                                    learning_rate = learning_rate,
                                    max_depth = max_depth,
                                    min_child_weight = min_child_weight,
                                    gamma = gamma, subsample = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def tuningHypercolsample_bytree(X, y, n_estimators, learning_rate, 
                                max_depth, min_child_weight, gamma,
                                subsample,
                                tuning_list):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    best_score = 0
    best_parameter = 0
    for interest in tuning_list:
        xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                    num_class=5, n_estimators=n_estimators, 
                                    seed=42, n_jobs=-1, 
                                    learning_rate = learning_rate,
                                    max_depth = max_depth,
                                    min_child_weight = min_child_weight,
                                    gamma = gamma, subsample = subsample,
                                    colsample_bytree = interest) 
        xgmodel.fit(X_train, y_train)
        y_pred = xgmodel.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"xg Accuracy: {accuracy:.4f}")
        xgconf_mat = confusion_matrix(y_test, y_pred)
        print(xgconf_mat)
        print(f"Parameter: {interest}; Accuracy: {accuracy*100:.2f}%")
        if accuracy > best_score:
            best_score = accuracy
            best_parameter = interest
    return best_score, best_parameter

def testBestModel(X, y, **kwargs):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=42)
    xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                num_class=5, 
                                seed=42, n_jobs=-1, 
                                **kwargs) 
    xgmodel.fit(X_train, y_train)
    y_pred = xgmodel.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"CV xg Accuracy: {accuracy:.4f}")
    xgconf_mat = confusion_matrix(y_test, y_pred)
    print(xgconf_mat)
    xgmodel = xgb.XGBClassifier(objective='multi:softmax', eval_metric='mlogloss',
                                num_class=5, 
                                seed=42, n_jobs=-1, 
                                **kwargs) 
    xgmodel.fit(X, y)
    y_pred = xgmodel.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print(f"ALL xg Accuracy: {accuracy:.4f}")
    xgconf_mat = confusion_matrix(y, y_pred)
    print(xgconf_mat)
    print(**kwargs)
    return None

REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('n')


X, y = getXandY('LSoverall')
best_score, best_n_estimators = tuningHyperNestimator(X, y, 
                                                      [100, 200, 300, 400, 500,
                                                       600, 700, 800, 900, 1000,
                                                       1100, 1200, 1300, 1400,
                                                       1500, 1600, 1700, 1800,
                                                       1900, 2000, 2100, 2200, 
                                                       2300, 2400, 2500, 2600,
                                                       2700, 2800, 2900, 3000])
 
best_score, best_lr = tuningHyperLr(X, y, best_n_estimators, 
                                    [0.01, 0.05, 0.1, 0.2, 0.5, 0.6, 0.8])

best_score, best_maxdepth = tuningHyperMaxDepth(X, y, best_n_estimators, best_lr,
                                                [3, 4, 5, 6, 7, 8, 9, 10,
                                                 11, 12, 13, 14, 15])
 
best_score, best_child = tuningHyperChild(X, y, best_n_estimators, best_lr,
                                          best_maxdepth,
                                          [1, 2, 3, 4, 5, 
                                           6, 7, 8, 9, 10])
 
best_score, best_gamma = tuningHyperGamma(X, y, best_n_estimators, best_lr,
                                          best_maxdepth, best_child,
                                          [0, 1, 2, 3, 4, 5])
 
best_score, best_Subsample = tuningHyperSubsample(X, y, best_n_estimators, best_lr,
                                                  best_maxdepth, best_child, best_gamma,
                                                  [0.5, 0.6, 0.7, 0.8, 0.9, 1])
 
best_score, best_colsample_bytree = tuningHypercolsample_bytree(X, y, best_n_estimators, best_lr,
                                                                best_maxdepth, best_child,
                                                                best_gamma,
                                                                best_Subsample,
                                                                [0.1, 0.2, 0.3, 0.4, 0.5,
                                                                 0.6, 0.7, 0.8, 0.9, 1])
testBestModel(X, y, n_estimators = best_n_estimators, 
              learning_rate = best_lr,
              max_depth = best_maxdepth, min_child_weight = best_child,
              gamma = best_gamma, subsample = best_Subsample, 
              colsample_bytree = best_colsample_bytree)

"""
n_estimators=1800, learning_rate = interest,
max_depth = max_depth, min_child_weight = min_child_weight,
gamma = gamma, subsample = subsample, colsample_bytree = colsample_bytree

"""
