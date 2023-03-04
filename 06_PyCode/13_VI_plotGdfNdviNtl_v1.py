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
import matplotlib.colors
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

def readGdfFromDisk():
    japan_perfecture = gpd.read_file("/mnt/g/17_Article/01_Data/00_mesh/gadm40_JPN_1.shp")
    return japan_perfecture

REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('wsl')
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green", "white", "yellow","red"])
JAPAN_PERFECTURE = readGdfFromDisk()

Output_Variable = 'LSoverall'
MV_Location_Df_LSoverall = load(REPO_RESULT_LOCATION + "MediumMedium/11_MV_Location_Df_" + Output_Variable +".joblib")
income_spatialcoefficient_LSoverall = load(REPO_RESULT_LOCATION + "MediumMedium/10_income_spatialcoefficient_" + Output_Variable +".joblib")
MV_Location_Df_LSoverall = pd.concat([MV_Location_Df_LSoverall, income_spatialcoefficient_LSoverall], axis=1)

gdf = gpd.GeoDataFrame(
    MV_Location_Df_LSoverall, 
    geometry=gpd.points_from_xy(MV_Location_Df_LSoverall.lon, MV_Location_Df_LSoverall.lat))

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NDVI_coef', cmap=CMAP, legend=True, markersize=1,
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NTL_coef', cmap=CMAP, legend=True, markersize=1,
         ax = ax, vmin = -0.002, vmax = 0.002, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NTL_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='income_indiv_coef', cmap='Reds', legend=True, markersize=1,
         ax = ax, vmin = 0, vmax = 0.02, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "income_indiv_coef.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NDVI_MV', cmap=CMAP, legend=True, markersize=1,
         ax = ax, vmin = -0.02, vmax = 0.02, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NDVI_MV.jpg", bbox_inches='tight')

fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
JAPAN_PERFECTURE.plot(ax=ax, color='#F6F6F6', alpha = 0.5)
JAPAN_PERFECTURE.boundary.plot(ax=ax, edgecolor='black', alpha = 0.5, linewidth=0.1)
gdf.plot(column='NTL_MV', cmap=CMAP, legend=True, markersize=1,
         ax = ax, vmin = -0.015, vmax = 0.015, alpha = 0.3)
plt.grid(linestyle='dashed')
plt.xlim(126, 146)
plt.ylim(26,46)
fig.savefig(REPO_FIGURE_LOCATION + "NTL_MV.jpg", bbox_inches='tight')
