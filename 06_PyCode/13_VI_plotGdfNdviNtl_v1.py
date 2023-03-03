# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 12:49:06 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""



import geopandas as gpd
from joblib import load
import matplotlib.pyplot as plt
import pandas as pd

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


REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')

Output_Variable = 'LSoverall'
MV_Location_Df_LSoverall = load(REPO_RESULT_LOCATION + "11_MV_Location_Df_" + Output_Variable +".joblib")
income_spatialcoefficient_LSoverall = load(REPO_RESULT_LOCATION + "10_income_spatialcoefficient_" + Output_Variable +".joblib")
MV_Location_Df_LSoverall = pd.concat([MV_Location_Df_LSoverall, income_spatialcoefficient_LSoverall], axis=1)

gdf = gpd.GeoDataFrame(
    MV_Location_Df_LSoverall, 
    geometry=gpd.points_from_xy(MV_Location_Df_LSoverall.lon, MV_Location_Df_LSoverall.lat))

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
gdf.plot(column='NDVI_coef', cmap='RdBu_r', legend=True, markersize=1,
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.5)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
gdf.plot(column='NTL_coef', cmap='RdBu_r', legend=True, markersize=1,
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.5)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NTL_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
gdf.plot(column='income_indiv_coef', cmap='Reds', legend=True, markersize=1,
         ax = ax, vmin = 0, vmax = 0.02, alpha = 0.5)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "income_indiv_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
gdf.plot(column='NDVI_MV', cmap='RdBu_r', legend=True, markersize=1,
         ax = ax, vmin = -0.02, vmax = 0.02, alpha = 0.5)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_MV.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
gdf.plot(column='NTL_MV', cmap='RdBu_r', legend=True, markersize=1,
         ax = ax, vmin = -0.015, vmax = 0.015, alpha = 0.5)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NTL_MV.jpg", bbox_inches='tight')
