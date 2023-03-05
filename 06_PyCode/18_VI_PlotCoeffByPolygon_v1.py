# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:17:14 2023

@author: chaol

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import geopandas as gpd
from joblib import load
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import box


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

def readGdfFromDisk():
    japan_perfecture = gpd.read_file("G:/17_Article/01_Data/00_mesh/gadm40_JPN_1.shp")
    meshGDF = gpd.read_file("G:/17_Article/01_Data/00_mesh/Mesh500/mergedPointMesh500m.shp")
    meshGDF.G04c_001 = meshGDF.G04c_001.astype('int64')
    meshGDF = meshGDF.set_index("G04c_001")
    meshGDF = meshGDF.set_crs(4326)
    meshPoly = gpd.read_file("G:/17_Article/01_Data/00_mesh/Mesh500/mergedPolyMesh500m.shp")
    meshPoly.G04c_001 = meshPoly.G04c_001.astype('int64')
    meshPoly = meshPoly.set_index("G04c_001")
    meshPoly = meshPoly.set_crs(4326)
    return japan_perfecture, meshGDF, meshPoly

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


def run(Output_Variable):
    gdf = getCoefGdf(Output_Variable)
    
    NDVI_Coef_Point = []
    
    for i in list(range(8)):
        MESHGDF_Single = MESHGDF.iloc[200000*i:200000*(1+i),:]
        NDVI_Coef_Point_Single = gpd.sjoin(gdf, MESHGDF_Single, how="right", op="contains")
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single[['NDVI_coef', 'NTL_coef', "income_indiv_coef"]]
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single.reset_index()
        NDVI_Coef_Point_Single = NDVI_Coef_Point_Single.groupby('G04c_001', as_index=False).mean()
        NDVI_Coef_Point.append(NDVI_Coef_Point_Single)
        print(f"now: {i}")
    NDVI_Coef_Df = pd.concat(NDVI_Coef_Point, axis=0)
    NDVI_Coef_Df.to_pickle(REPO_RESULT_LOCATION + "16_PointAverageCoef_" + Output_Variable + ".pkl")
    return None

def getGdf(Output_Variable, MESHPOLY):
    gdf = getCoefGdf(Output_Variable)
    NDVI_Coef_Df = pd.read_pickle(REPO_RESULT_LOCATION + "16_PointAverageCoef_" + Output_Variable + ".pkl")
    NDVI_Coef_Df = NDVI_Coef_Df.set_index('G04c_001')
    NDVI_Coef_Gdf = gpd.GeoDataFrame(pd.concat([NDVI_Coef_Df, MESHPOLY], axis=1))
    return NDVI_Coef_Gdf

def plotOverlapCoeff(NDVI_Coef_Gdf, Output_Label):
    ov_standard_dict = {"LSoverall":"OVLS", "LSrelative":"RLS",
                        "Happinessoverall":"OH", "Happinessrelative":"RH"}
    NDVI_Coef_Gdf['MV_NDVI'] = NDVI_Coef_Gdf['NDVI_coef'] / NDVI_Coef_Gdf['income_indiv_coef']
    NDVI_Coef_Gdf['MV_NTL'] = NDVI_Coef_Gdf['NTL_coef'] / NDVI_Coef_Gdf['income_indiv_coef']
    NDVI_Coef_Gdf.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    vmin = -0.0004
    vmax = 0.0004
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
    JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    NDVI_Coef_Gdf.plot(column='NDVI_coef', ax=ax, legend=True, cmap=CMAP, 
             vmax = vmax, vmin = vmin)
    plt.title("NDVI Coefficient (Output: " + Output_Label + ")", loc = "left")
    plt.grid(linestyle='dashed')
    plt.xlim(126, 146)
    plt.ylim(26,46)
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "NDVI_coef_polygon_average_"+Output_Variable +".jpg",
                dpi = 1000, bbox_inches='tight')
    
    vmin = -0.003
    vmax = 0.003
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
    JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    NDVI_Coef_Gdf.plot(column='NTL_coef', ax=ax, legend=True, cmap=CMAP, 
             vmax = vmax, vmin = vmin)
    plt.title("NTL Coefficient (Output: " + Output_Label + ")", loc = "left")
    plt.grid(linestyle='dashed')
    plt.xlim(126, 146)
    plt.ylim(26,46)
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "NTL_coef_polygon_average_"+Output_Variable +".jpg",
                dpi = 1000, bbox_inches='tight')
    
    vmin = -0.018
    vmax = 0.018
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
    JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    NDVI_Coef_Gdf.plot(column='income_indiv_coef', ax=ax, legend=True, cmap=CMAP, 
             vmax = vmax, vmin = vmin)
    plt.title("Income Coefficient (Output: " + Output_Label + ")", loc = "left")
    plt.grid(linestyle='dashed')
    plt.xlim(126, 146)
    plt.ylim(26,46)
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "Income_coef_polygon_average_"+Output_Variable +".jpg",
                dpi = 1000, bbox_inches='tight')
    
    cmap_mv_ndvi = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", "yellow","red"])
    vmin = 0.012
    vmax = 0.025
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
    JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    NDVI_Coef_Gdf.plot(column='MV_NDVI', ax=ax, legend=True, cmap=cmap_mv_ndvi , 
             vmax = vmax, vmin = vmin)
    plt.title("Monetary Value of NDVI (Output: " + Output_Label + ")", loc = "left")
    plt.grid(linestyle='dashed')
    plt.xlim(126, 146)
    plt.ylim(26,46)
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "NDVI_mv_polygon_average_"+Output_Variable +".jpg",
                dpi = 1000, bbox_inches='tight')
    
    cmap_mv_ntl = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green", "white"])
    vmin = -0.160
    vmax = -0.080
    fig = plt.figure(figsize=(8, 8), dpi=1000)
    ax = plt.axes()
    JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
    JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
    NDVI_Coef_Gdf.plot(column='MV_NTL', ax=ax, legend=True, cmap=cmap_mv_ntl, 
             vmax = vmax, vmin = vmin)
    plt.title("Monetary Value of NTL (Output: " + Output_Label + ")", loc = "left")
    plt.grid(linestyle='dashed')
    plt.xlim(126, 146)
    plt.ylim(26,46)
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "NTL_mv_polygon_average_"+Output_Variable +".jpg",
                dpi = 1000, bbox_inches='tight')
    return None

Output_Variable = 'LSoverall'
REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green", "white", "yellow","red"])
JAPAN_PERFECTURE, MESHGDF, MESHPOLY = readGdfFromDisk()
#run('LSoverall')
#run("LSrelative")
#run("Happinessoverall")
#run("Happinessrelative")
NDVI_Coef_Gdf_OVLS = getGdf('LSoverall', MESHPOLY)


"""
fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NDVI_coef', cmap=CMAP, legend=True, 
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_poly_coef.jpg", bbox_inches='tight')
"""


