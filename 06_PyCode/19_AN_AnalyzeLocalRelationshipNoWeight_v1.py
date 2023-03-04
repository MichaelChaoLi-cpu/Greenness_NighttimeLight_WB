# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 14:17:12 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""


from glob import glob
from joblib import dump, load
import joblib
import numpy as np
import pandas as pd
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
    return X, y

def SpatialCoefficientBetweenLandCoverAndItsShap(variable_name, result, neighborList):
    coef_mat = joblib.Parallel(n_jobs=10)(
        joblib.delayed(singleCoefficientBetweenLandCoverAndItsShap)(neighbors, variable_name,
                                                                      result, obs_count)
        for obs_count, neighbors in enumerate(neighborList))
    coef_mat = pd.DataFrame(np.array(coef_mat))
    coef_mat.columns = [variable_name+'_coef', variable_name+'_interc',
                        variable_name+'_t_coef', variable_name+'_t_interc']
    
    return coef_mat

def singleCoefficientBetweenLandCoverAndItsShap(neighbors, variable_name, 
                                                  result, obs_count):
    result_selected = result.loc[neighbors,:]
    result_selected_location = result_selected[['lon', 'lat']]
    result_itself_location = result.iloc[[obs_count],:]
    result_selected = result_selected[[variable_name, variable_name+'_shap']]
    X_data = result_selected[[variable_name]]
    y = np.array(result_selected[[variable_name+'_shap']])
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

def run(Output_Variable):
    X, y = makeModel(Output_Variable)
    
    leftRightBoundary = load(REPO_RESULT_LOCATION + "05_leftRightBoundary_" + Output_Variable +".joblib")
    upDownBoundary = load(REPO_RESULT_LOCATION + "06_upDownBoundary_" + Output_Variable +".joblib")
    neighborList = load(REPO_RESULT_LOCATION + "07_neighborList_" + Output_Variable +".joblib")
    
    result = getMergeSHAPresult(Output_Variable)
    NDVI_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShap('NDVI', result, neighborList)
    NTL_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShap('NTL', result, neighborList)
    income_spatialcoefficient = SpatialCoefficientBetweenLandCoverAndItsShap('income_indiv', result, neighborList)
    dump(NDVI_spatialcoefficient, REPO_RESULT_LOCATION + "12_NDVI_spatialcoefficient_noweight_" + Output_Variable +".joblib")
    dump(NTL_spatialcoefficient, REPO_RESULT_LOCATION + "13_NTL_spatialcoefficient_noweight_" + Output_Variable +".joblib")
    dump(income_spatialcoefficient, REPO_RESULT_LOCATION + "14_income_spatialcoefficient_noweight_" + Output_Variable +".joblib")
    
    NDVI_spatialcoefficient_sig = keepSignificantValue(NDVI_spatialcoefficient)
    NTL_spatialcoefficient_sig = keepSignificantValue(NTL_spatialcoefficient)
    income_spatialcoefficient_sig = keepSignificantValue(income_spatialcoefficient)
    
    NDVI_MV = calculateMonetaryValue(NDVI_spatialcoefficient_sig, income_spatialcoefficient_sig, 'NDVI_MV')
    NTL_MV = calculateMonetaryValue(NTL_spatialcoefficient_sig, income_spatialcoefficient_sig, 'NTL_MV')
    
    lon_lat_df = getLonLatId(X)
    MV_Location_Df = pd.concat([lon_lat_df, NDVI_MV, NTL_MV], axis=1)
    dump(MV_Location_Df, REPO_RESULT_LOCATION + "15_MV_Location_Df_noweight_" + Output_Variable +".joblib")
    return None

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')

run('LSoverall')
run('LSrelative')
run('Happinessoverall')
run('Happinessrelative')



