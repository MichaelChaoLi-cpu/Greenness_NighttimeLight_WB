# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 12:45:18 2023

@author: Li Chao

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""

import matplotlib as mpl
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
    return repo_location, repo_result_location

def plotScatterColoredByOther(Variable_Of_Interest, y_Lim, Other_Variable, 
                              Bueatiful_Other_Name):
    dataframe_OVLS = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_LSoverall.csv", index_col = 0)
    dataframe_RLS = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_LSrelative.csv", index_col = 0)
    dataframe_OH = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_Happinessoverall.csv", index_col = 0)
    dataframe_RH = pd.read_csv(REPO_RESULT_LOCATION + "00_mergedXSHAP_Happinessrelative.csv", index_col = 0)
    
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(20.5, 17), dpi=300,
                            gridspec_kw={'height_ratios': [10, 10, 0.5]}) 
    ax_legend = fig.add_axes([0.1, 0.075, 0.8, 0.02])
    axs[0,0].scatter(dataframe_OVLS[Variable_Of_Interest], 
                           dataframe_OVLS[Variable_Of_Interest + "_shap"], 
                           c = dataframe_OVLS[Other_Variable], cmap=CMAP,
                           alpha=0.2, marker='.', edgecolors='none')
    axs[0,0].set_ylim([-y_Lim, y_Lim])
    axs[0,0].text(0.01, 0.99, "a", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[0,0].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[0,0].grid(linestyle='dashed')
    axs[0,0].set_xlabel(Variable_Of_Interest, fontsize=15)
    axs[0,0].set_ylabel(Variable_Of_Interest + " Shapley Value for OVLS", 
                        fontsize=15)
    
    axs[0,1].scatter(dataframe_RLS[Variable_Of_Interest], 
                           dataframe_RLS[Variable_Of_Interest + "_shap"], 
                           c = dataframe_RLS[Other_Variable], cmap=CMAP,
                           alpha=0.2, marker='.', edgecolors='none')
    axs[0,1].set_ylim([-y_Lim, y_Lim])
    axs[0,1].text(0.01, 0.99, "b", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[0,1].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[0,1].grid(linestyle='dashed')
    axs[0,1].set_xlabel(Variable_Of_Interest, fontsize=15)
    axs[0,1].set_ylabel(Variable_Of_Interest + " Shapley Value for RLS", 
                        fontsize=15)
    
    axs[1,0].scatter(dataframe_OH[Variable_Of_Interest], 
                           dataframe_OH[Variable_Of_Interest + "_shap"], 
                           c = dataframe_OH[Other_Variable], cmap=CMAP,
                           alpha=0.2, marker='.', edgecolors='none')
    axs[1,0].set_ylim([-y_Lim, y_Lim])
    axs[1,0].text(0.01, 0.99, "c", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[1,0].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[1,0].grid(linestyle='dashed')
    axs[1,0].set_xlabel(Variable_Of_Interest, fontsize=15)
    axs[1,0].set_ylabel(Variable_Of_Interest + " Shapley Value for OH", 
                        fontsize=15)
    
    axs[1,1].scatter(dataframe_RH[Variable_Of_Interest], 
                           dataframe_RH[Variable_Of_Interest + "_shap"], 
                           c = dataframe_RH[Other_Variable], cmap=CMAP,
                           alpha=0.2, marker='.', edgecolors='none')
    axs[1,1].set_ylim([-y_Lim, y_Lim])
    axs[1,1].text(0.01, 0.99, "d", 
                  fontsize = 16, horizontalalignment = "left", transform=axs[1,1].transAxes,
                  ha='left', va='top', fontweight='bold')
    axs[1,1].grid(linestyle='dashed')
    axs[1,1].set_xlabel(Variable_Of_Interest, fontsize=15)
    axs[1,1].set_ylabel(Variable_Of_Interest + " Shapley Value for RH", 
                        fontsize=15)
    
    axs[2, 0].axis('off')
    axs[2, 1].axis('off')
    vmin = dataframe_RH[Other_Variable].min()
    vmax = dataframe_RH[Other_Variable].max()
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP),
                        cax=ax_legend, orientation='horizontal')
    cbar.set_label(Bueatiful_Other_Name,size=15)
    cbar.ax.tick_params(labelsize=15) 
    
    plt.show();
    fig.savefig(REPO_FIGURE_LOCATION + Variable_Of_Interest + '_' + Other_Variable + ".jpg",
                dpi = 300, bbox_inches='tight')
    return None

REPO_LOCATION, REPO_RESULT_LOCATION = runLocallyOrRemotely('y')
REPO_FIGURE_LOCATION = REPO_LOCATION + "04_Figure/"
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","green","yellow","red"])

plotScatterColoredByOther('NDVI', 0.1, 'easy_to_relax', 'Easy to Relax')
plotScatterColoredByOther('NDVI', 0.1, 'high_stress', 'Frequency of High-level Stress')
plotScatterColoredByOther('NDVI', 0.1, 'low_stress', 'Frequency of Low-level Stress')

plotScatterColoredByOther('NTL', 0.2, 'easy_to_relax', 'Easy to Relax')
plotScatterColoredByOther('NTL', 0.2, 'high_stress', 'Frequency of High-level Stress')
plotScatterColoredByOther('NTL', 0.2, 'low_stress', 'Frequency of Low-level Stress')




