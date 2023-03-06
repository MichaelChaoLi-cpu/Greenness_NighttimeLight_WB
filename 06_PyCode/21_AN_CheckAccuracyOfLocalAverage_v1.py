# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:39:45 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

from glob import glob
import geopandas as gpd
from joblib import load
import numpy as np
import pandas as pd
from shapely.geometry import box, Point
from sklearn.metrics import r2_score


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


def getCoefGdf(Output_Variable):
    leftRightBoundary = load(REPO_RESULT_LOCATION + "05_leftRightBoundary_" + Output_Variable +".joblib")
    upDownBoundary = load(REPO_RESULT_LOCATION + "06_upDownBoundary_" + Output_Variable +".joblib")
    NDVI_spatialcoefficient = pd.read_csv(REPO_RESULT_LOCATION + "08_NDVI_spatialcoefficient_" + Output_Variable +".csv",
                                          index_col=0)
    NTL_spatialcoefficient = pd.read_csv(REPO_RESULT_LOCATION + "09_NTL_spatialcoefficient_" + Output_Variable +".csv",
                                         index_col=0)
    income_spatialcoefficient = pd.read_csv(REPO_RESULT_LOCATION + "10_income_spatialcoefficient_" + Output_Variable + ".csv",
                                            index_col=0)
    leftRightBoundary = pd.DataFrame(leftRightBoundary, columns=['left', 'right'])
    upDownBoundary = pd.DataFrame(upDownBoundary, columns=['bottom', 'top'])
    df = pd.concat([leftRightBoundary, upDownBoundary, NDVI_spatialcoefficient,
                    NTL_spatialcoefficient, income_spatialcoefficient], axis=1)
    geometry = [box(x1, y1, x2, y2) for x1, y1, x2, y2 in zip(df.left, df.bottom,
                                                              df.right, df.top)]
    df = df.drop(['left', 'right', 'bottom', 'top'], axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    gdf = gdf.set_crs(4326)
    return gdf

def getGdfOfRawData(Output_Variable):
    X = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_" + Output_Variable + ".csv", index_col=0)
    X = X[['lat', 'lon', 'income_indiv', 'NDVI', 'NTL', 
           'income_indiv_shap', 'NDVI_shap', 'NTL_shap']]
    geometry = [Point(xy) for xy in zip(X.lon, X.lat)]
    X = X.drop(['lon', 'lat'], axis=1) 
    gdf = gpd.GeoDataFrame(X, crs="EPSG:4326", geometry=geometry)
    return gdf

def getCoefOnPoint(Output_Variable):
    gdf = getCoefGdf(Output_Variable)
    point_location = getGdfOfRawData(Output_Variable)
    
    NDVI_Coef_Point = []
    
    for i in list(range(8)):
        point_location_single = point_location.iloc[50000*i:50000*(1+i),:]
        NDVI_Coef_Point_Single = gpd.sjoin(gdf, point_location_single, how="right", op="contains")
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single[['NDVI_coef', 'NDVI_interc', 'NTL_interc', 
                                                         'NTL_coef', 'income_indiv_coef', 
                                                         'income_indiv_interc']]
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single.reset_index()
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single.groupby('Unnamed: 0', as_index=False).mean()
        NDVI_Coef_Point.append(NDVI_Coef_Point_Single)
        print(f"now: {i}")

    NDVI_Coef_Df = pd.concat(NDVI_Coef_Point, axis=0)
    NDVI_Coef_Df.reset_index(inplace=True)
    NDVI_Coef_Df = NDVI_Coef_Df[['NDVI_coef', 'NDVI_interc', 'NTL_interc', 
                                 'NTL_coef', 'income_indiv_coef', 
                                 'income_indiv_interc']]
    NDVI_Coef_Df.to_pickle(REPO_RESULT_LOCATION + "17_DatasetLocationAverageCoef_" + Output_Variable + ".pkl")
    
    test_df = pd.concat([NDVI_Coef_Df, point_location.reset_index()], axis=1)
    test_df["NDVI_shap_pred"] = test_df['NDVI_coef'] * test_df['NDVI'] + test_df['NDVI_interc']
    print("NDVI R2:", r2_score(test_df["NDVI_shap"], test_df["NDVI_shap_pred"] ))
    
    test_df["NTL_shap_pred"] = test_df['NTL_coef'] * test_df['NTL'] + test_df['NTL_interc']
    print("NTL R2:", r2_score(test_df["NTL_shap"], test_df["NTL_shap_pred"] ))
    
    test_df["income_indiv_shap_pred"] = test_df['income_indiv_coef'] * test_df['income_indiv'] + test_df['income_indiv_interc']
    print("income_indiv R2:", r2_score(test_df["income_indiv_shap"], test_df["income_indiv_shap_pred"] ))
    return None

def getMvInformation(Output_Variable):
    NDVI_Coef_Df = pd.read_pickle(REPO_RESULT_LOCATION + "17_DatasetLocationAverageCoef_" + Output_Variable + ".pkl")
    point_location = getGdfOfRawData(Output_Variable)
    test_df = pd.concat([NDVI_Coef_Df, point_location.reset_index()], axis=1)
    test_df['MV_NDVI'] = test_df['NDVI_coef'] / test_df['income_indiv_coef'] * 1000000 / 121.0458
    test_df['MV_NTL'] = test_df['NTL_coef'] / test_df['income_indiv_coef'] * 1000000 / 121.0458
    test_df['MV_NDVI'].replace([np.inf, -np.inf], np.nan, inplace=True)
    test_df['MV_NTL'].replace([np.inf, -np.inf], np.nan, inplace=True)
    mean_NDVI = np.nanmean(test_df['MV_NDVI']) 
    SE_NDVI = np.std(test_df['MV_NDVI'], ddof=1) / np.sqrt(np.size(test_df['MV_NDVI']))
    mean_NTL = np.nanmean(test_df['MV_NTL']) 
    SE_NTL = np.std(test_df['MV_NTL'], ddof=1) / np.sqrt(np.size(test_df['MV_NTL']))
    print(f'NDVI mean {mean_NDVI:.2f}, 95%CI:{mean_NDVI-1.96*SE_NDVI:.2f} - {mean_NDVI+1.96*SE_NDVI:.2f}')
    print(f'NTL mean {mean_NTL:.2f}, 95%CI:{mean_NTL-1.96*SE_NTL:.2f} - {mean_NTL+1.96*SE_NTL:.2f}')
    return None

Output_Variable = 'LSoverall'
REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')
getCoefOnPoint('LSoverall')
getCoefOnPoint('LSrelative')
getCoefOnPoint('Happinessoverall')
getCoefOnPoint('Happinessrelative')

getMvInformation('LSoverall')
getMvInformation('LSrelative')
getMvInformation('Happinessoverall')
getMvInformation('Happinessrelative')

