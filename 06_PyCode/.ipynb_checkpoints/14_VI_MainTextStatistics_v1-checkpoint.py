# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 14:47:09 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""


from glob import glob
import matplotlib.pyplot as plt
import numpy as np
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

def plotSwbHist():
    Ovls_file_name = glob(REPO_LOCATION + "01_Data/*_y_LSoverall*.csv")
    Ovls = pd.read_csv(Ovls_file_name[0], index_col=0)
    Rls_file_name = glob(REPO_LOCATION + "01_Data/*_y_LSrelative*.csv")
    Rls = pd.read_csv(Rls_file_name[0], index_col=0)
    Oh_file_name = glob(REPO_LOCATION + "01_Data/*_y_Happinessoverall*.csv")
    Oh = pd.read_csv(Oh_file_name[0], index_col=0)
    Rh_file_name = glob(REPO_LOCATION + "01_Data/*_y_Happinessrelative*.csv")
    Rh = pd.read_csv(Rh_file_name[0], index_col=0)
    df = pd.concat([Ovls, Rls, Oh, Rh], axis=1)
    
    x_file_name = glob(REPO_LOCATION + "01_Data/*_X_LSoverall*.csv")
    df_x = pd.read_csv(x_file_name[0], index_col=0)
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(20, 16), dpi=300)
    axs[0,0].hist(df, bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5], 
                  label=["OVLS", "RLS", "OH", "RH"], edgecolor='black')
    axs[0,0].legend()
    axs[0,0].text(0.01, 0.95, "N: 383,173\nMean OVLS: 3.38\nMean RLS: 3.14\nMean OH: 3.61\nMean RH: 3.38", 
                  fontsize = 14, horizontalalignment = "left", transform=axs[0,0].transAxes,
                  ha='left', va='top')
    axs[0,0].text(0.01, 0.99, "a", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[0,0].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[0,0].grid(linestyle='dashed')
    axs[0,0].set_xlabel("SWB Assessment", fontsize=15)
    axs[0,0].set_ylabel("Frequency", fontsize=15)
    
    axs[0,1].hist(df_x.NDVI, bins=50, color='limegreen', edgecolor='black')
    axs[0,1].text(0.01, 0.95, "N: 383,173\nMean NDVI: 36.25", 
                  fontsize = 14, horizontalalignment = "left", transform=axs[0,1].transAxes,
                  ha='left', va='top')
    axs[0,1].text(0.01, 0.99, "b", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[0,1].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[0,1].grid(linestyle='dashed')
    axs[0,1].set_xlabel("NDVI (%)", fontsize=15)
    axs[0,1].set_ylabel("Frequency", fontsize=15)
    
    axs[1,0].hist(df_x.NTL, bins=50, color='orange', edgecolor='black')
    axs[1,0].text(0.70, 0.95, "N: 383,173\nMean NTL: 18.59", 
                  fontsize = 14, horizontalalignment = "left", transform=axs[1,0].transAxes,
                  ha='left', va='top')
    axs[1,0].text(0.97, 0.99, "c", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[1,0].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[1,0].grid(linestyle='dashed')
    axs[1,0].set_xlabel("NTL (nw/$cm^2$ sr)", fontsize=15)
    axs[1,0].set_ylabel("Frequency", fontsize=15)
    
    axs[1,1].hist(df_x.income_indiv, color='cyan', edgecolor='black', bins=28)
    axs[1,1].text(0.70, 0.95, "N: 383,173\nMean Income: 4.69", 
                  fontsize = 14, horizontalalignment = "left", transform=axs[1,1].transAxes,
                  ha='left', va='top')
    axs[1,1].text(0.97, 0.99, "d", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[1,1].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[1,1].grid(linestyle='dashed')
    axs[1,1].set_xlabel("Income (Million)", fontsize=15)
    axs[1,1].set_ylabel("Frequency", fontsize=15)
    
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + "Distribution_output.jpg",
                dpi = 300, bbox_inches='tight')
    return None
    

REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely('y')
plotSwbHist()
