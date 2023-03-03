# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:35:49 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

from sklearn.ensemble import RandomForestRegressor
from glob import glob
import pandas as pd
import numpy as np

from joblib import dump
import joblib

from sklearn.linear_model import LinearRegression

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

def makeModel(Variable_Of_Interest):
    X_file_name = glob(REPO_LOCATION + "01_Data/*_X_" + Variable_Of_Interest + "*.csv")
    X = pd.read_csv(X_file_name[0], index_col=0)
    y_file_name = glob(REPO_LOCATION + "01_Data/*_y_" + Variable_Of_Interest + "*.csv")
    y = pd.read_csv(y_file_name[0], index_col=0)
    model = RandomForestRegressor(n_estimators=1000, min_samples_split = 100, 
                                  max_features = 7, random_state=1, n_jobs=-1)
    model.fit(X, y)
    return model, X, y


### define function
def XYSplit(model):
    total_tree_number = model.n_estimators
    X_split_array = []
    Y_split_array = []
    for tree_order in list(range(total_tree_number)):
        feature = model.estimators_[tree_order].tree_.feature
        threshold = model.estimators_[tree_order].tree_.threshold
        
        df = pd.concat([pd.Series(feature), pd.Series(threshold)], axis=1)
        df.columns = ['feature', 'threshold']
        X_split = df[df['feature']==2]
        Y_split = df[df['feature']==1]
        
        X_split = X_split.sort_values('threshold')
        Y_split = Y_split.sort_values('threshold')
        X_split = np.array(X_split.threshold, dtype='float64')
        Y_split = np.array(Y_split.threshold, dtype='float64')
        
        X_split_array.append(X_split)
        Y_split_array.append(Y_split)
        
    return (X_split_array, Y_split_array)

def findBoundaryArray(split_array, data_degree):
    boundary_array = joblib.Parallel(n_jobs=10)(
        joblib.delayed(findBoundary)(split_array, observation)
        for observation in data_degree)
        
    return boundary_array
    
    
def findBoundary(split_array, observation):
    before_array = []
    after_array = []
    for split in split_array:
        split_add = np.insert(split, 0, observation)
        split_add = np.sort(split_add)
        location = np.where(split_add == observation)[0][0]
        if location == 0:
            before = observation - 1
        else:
            before = split[location - 1]
        if location == len(split_add)-1:
            after = observation + 1
        else:
            after = split[location]
        before_array.append(before)
        after_array.append(after)
    #before_observation = np.min(np.array(before_array))
    #after_observation = np.max(np.array(after_array))
    #before_observation = np.median(np.array(before_array))
    #after_observation = np.median(np.array(after_array))
    before_observation = np.quantile(np.array(before_array), 0.75)
    after_observation = np.quantile(np.array(after_array), 0.25)
    return [before_observation, after_observation]

def buildNeighborList(data, leftRightBoundary, upDownBoundary):
    data = pd.DataFrame(data.iloc[:, 1:3], columns=['lat', 'lon'])
    index_select_array = []
    for obs_order in list(range(len(data))):
         data_select = data[
             (data['lon'] > leftRightBoundary[obs_order][0]) &
             (data['lon'] < leftRightBoundary[obs_order][1]) &
             (data['lat'] > upDownBoundary[obs_order][0]) &
             (data['lat'] < upDownBoundary[obs_order][1])
             ]
         index_select = np.array(data_select.index)
         index_select_array.append(index_select)
    return index_select_array

def SpatialCoefficientBetweenLandCoverAndItsShapGw(variable_name, result, neighborList):
    coef_mat = joblib.Parallel(n_jobs=10)(
        joblib.delayed(singleCoefficientBetweenLandCoverAndItsShapGw)(neighbors, variable_name,
                                                                      result, obs_count)
        for obs_count, neighbors in enumerate(neighborList))
    coef_mat = pd.DataFrame(np.array(coef_mat))
    coef_mat.columns = [variable_name+'_coef', variable_name+'_interc',
                        variable_name+'_t_coef', variable_name+'_t_interc']
    
    return coef_mat

def singleCoefficientBetweenLandCoverAndItsShapGw(neighbors, variable_name, 
                                                  result, obs_count):
    result_selected = result.loc[neighbors,:]
    result_selected_location = result_selected[['lon', 'lat']]
    result_itself_location = result.iloc[[obs_count],:]
    distance_array = np.sqrt(np.array((result_selected_location.loc[:,'lon'] -  result_itself_location.iloc[0, 2])**2 + (result_selected_location.loc[:,'lat'] -  result_itself_location.iloc[0, 1])**2))
    bandwidth = max(distance_array)
    print(obs_count, bandwidth)
    weights = (1 - (distance_array/bandwidth)**2)**2
    weights = np.nan_to_num(weights, nan=1)
    result_selected = result_selected[[variable_name, variable_name+'_shap']]
    X_data = result_selected[[variable_name]]
    y = np.array(result_selected[[variable_name+'_shap']])
    try:
        reg = LinearRegression().fit(X_data, y, sample_weight=weights)
    except:
        reg = LinearRegression().fit(X_data, y)
    predictions = reg.predict(X_data)
    newX = X_data
    newX['Constant'] = 1
    try:
        MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))
        var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
        sd_b = np.sqrt(var_b) 
        t_coef = reg.coef_[0][0]/sd_b[0]
        t_interc = reg.intercept_[0]/sd_b[1]
    except:
        t_coef=0
        t_interc=0
    coef = reg.coef_[0][0]
    intercept = reg.intercept_[0]
    return [coef, intercept, t_coef, t_interc]

def getMergeSHAPresult(Variable_Of_Interest):
    result = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_" + Variable_Of_Interest + ".csv", index_col=0)
    return result

def keepSignificantValue(Spatial_Coefficient_Df):
    Spatial_Coefficient_Df.fillna(0, inplace=True)
    Spatial_Coefficient_Df.loc[abs(Spatial_Coefficient_Df[Spatial_Coefficient_Df.columns.values[2]]) < 1.64, 
                               Spatial_Coefficient_Df.columns.values[0]] = 0
    Spatial_Coefficient_Df.loc[abs(Spatial_Coefficient_Df[Spatial_Coefficient_Df.columns.values[3]]) < 1.64,
                               Spatial_Coefficient_Df.columns.values[1]] = 0
    return Spatial_Coefficient_Df

def calculateMonetaryValue(Interest_Coeff_Df, Income_Coeff_Df, Mv_Name):
    Interest_Coeff_Df[Mv_Name] = Interest_Coeff_Df[Interest_Coeff_Df.columns.values[0]]/Income_Coeff_Df[Income_Coeff_Df.columns.values[0]]
    Interest_Coeff_Df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    return Interest_Coeff_Df

def getLonLatId(X):
    lon_lat_df = X.reset_index()
    lon_lat_df = lon_lat_df[['index', 'lon', 'lat']]
    return lon_lat_df

Output_Variable = 'LSoverall'
REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')

def run(Output_Variable):
    model, X, y = makeModel(Output_Variable)
    
    X_split_array, Y_split_array = XYSplit(model)
    leftRightBoundary = findBoundaryArray(X_split_array, X.iloc[:,2])
    upDownBoundary = findBoundaryArray(Y_split_array, X.iloc[:,1])
    neighborList = buildNeighborList(X, leftRightBoundary, upDownBoundary)
    dump(leftRightBoundary, REPO_RESULT_LOCATION + "05_leftRightBoundary_" + Output_Variable +".joblib")
    dump(upDownBoundary, REPO_RESULT_LOCATION + "06_upDownBoundary_" + Output_Variable +".joblib")
    dump(neighborList, REPO_RESULT_LOCATION + "07_neighborList_" + Output_Variable +".joblib")
    
    result = getMergeSHAPresult(Output_Variable)
    NDVI_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShapGw('NDVI', result, neighborList)
    NTL_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShapGw('NTL', result, neighborList)
    income_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShapGw('income_indiv', result, neighborList)
    dump(NDVI_spatialcoefficient, REPO_RESULT_LOCATION + "08_NDVI_spatialcoefficient_" + Output_Variable +".joblib")
    dump(NTL_spatialcoefficient, REPO_RESULT_LOCATION + "09_NTL_spatialcoefficient_" + Output_Variable +".joblib")
    dump(income_spatialcoefficient, REPO_RESULT_LOCATION + "10_income_spatialcoefficient_" + Output_Variable +".joblib")
    
    NDVI_spatialcoefficient_sig = keepSignificantValue(NDVI_spatialcoefficient)
    NTL_spatialcoefficient_sig = keepSignificantValue(NTL_spatialcoefficient)
    income_spatialcoefficient_sig = keepSignificantValue(income_spatialcoefficient)
    
    NDVI_MV = calculateMonetaryValue(NDVI_spatialcoefficient_sig, income_spatialcoefficient_sig, 'NDVI_MV')
    NTL_MV = calculateMonetaryValue(NTL_spatialcoefficient_sig, income_spatialcoefficient_sig, 'NTL_MV')
    
    lon_lat_df = getLonLatId(X)
    MV_Location_Df = pd.concat([lon_lat_df, NDVI_MV, NTL_MV], axis=1)
    dump(MV_Location_Df, REPO_RESULT_LOCATION + "11_MV_Location_Df_" + Output_Variable +".joblib")
    return None

run('LSoverall')
run('LSrelative')
run('Happinessoverall')
run('Happinessrelative')

"""
from joblib import load

leftRightBoundary = load(REPO_RESULT_LOCATION + "05_leftRightBoundary.joblib")
upDownBoundary = load(REPO_RESULT_LOCATION + "06_upDownBoundary.joblib")
neighborList = load(REPO_RESULT_LOCATION + "07_neighborList.joblib")

# median
def findBoundary(split_array, observation):
    before_array = []
    after_array = []
    for split in split_array:
        split_add = np.insert(split, 0, observation)
        split_add = np.sort(split_add)
        location = np.where(split_add == observation)[0][0]
        if location == 0:
            before = observation - 1
        else:
            before = split[location - 1]
        if location == len(split_add)-1:
            after = observation + 1
        else:
            after = split[location]
        before_array.append(before)
        after_array.append(after)
    before_observation = np.median(np.array(before_array))
    after_observation = np.median(np.array(after_array))
    #before_observation = np.min(np.array(before_array))
    #after_observation = np.max(np.array(after_array))
    return [before_observation, after_observation]
"""
