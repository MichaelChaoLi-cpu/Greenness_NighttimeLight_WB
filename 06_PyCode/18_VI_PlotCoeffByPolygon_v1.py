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
    return japan_perfecture, meshGDF

def getCoefGdf(Output_Variable):
    leftRightBoundary = load(REPO_RESULT_LOCATION + "05_leftRightBoundary_" + Output_Variable +".joblib")
    upDownBoundary = load(REPO_RESULT_LOCATION + "06_upDownBoundary_" + Output_Variable +".joblib")
    NDVI_spatialcoefficient = pd.read_csv(REPO_RESULT_LOCATION + "08_NDVI_spatialcoefficient_" + Output_Variable +".csv",
                                          index_col=0)
    NTL_spatialcoefficient = pd.read_csv(REPO_RESULT_LOCATION + "09_NTL_spatialcoefficient_" + Output_Variable +".csv",
                                         index_col=0)
    leftRightBoundary = pd.DataFrame(leftRightBoundary, columns=['left', 'right'])
    upDownBoundary = pd.DataFrame(upDownBoundary, columns=['bottom', 'top'])
    df = pd.concat([leftRightBoundary, upDownBoundary, NDVI_spatialcoefficient,
                    NTL_spatialcoefficient], axis=1)
    geometry = [box(x1, y1, x2, y2) for x1, y1, x2, y2 in zip(df.left, df.bottom,
                                                              df.right, df.top)]
    df = df.drop(['left', 'right', 'bottom', 'top'], axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    gdf = gdf.set_crs(4326)
    return gdf



Output_Variable = 'LSoverall'
REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green", "white", "yellow","red"])
JAPAN_PERFECTURE, MESHGDF = readGdfFromDisk()

gdf = getCoefGdf(Output_Variable)

NDVI_Coef_Point = gpd.sjoin(gdf, MESHGDF, how="right", op="contains")

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NDVI_coef', cmap=CMAP, legend=True, 
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_poly_coef.jpg", bbox_inches='tight')
