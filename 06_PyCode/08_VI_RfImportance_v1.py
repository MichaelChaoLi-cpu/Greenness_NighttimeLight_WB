# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:39:26 2022

@author: li.chao.987@s.kyushu-u.ac.jp

NOTE: 
    GLOBAL_VARIABLE
    local_variable
    functionToRun
    Function_Input_Or_Ouput_Variable
"""


from joblib import load
import matplotlib.pyplot as plt
import numpy as np
from sklearn.inspection import permutation_importance

def runLocallyOrRemotely(Locally_Or_Remotely):
    locally_or_remotely = Locally_Or_Remotely
    if locally_or_remotely == 'y':
        repo_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
        repo_figure_location = "D:/OneDrive - Kyushu University/15_Article/03_RStudio/04_Figure/"
    elif locally_or_remotely == 'n':
        repo_location = "/home/usr6/q70176a/DP15/"
        repo_result_location = "/home/usr6/q70176a/DP15/03_Results/"
        repo_figure_location = "/home/usr6/q70176a/DP15/04_Figure/"
    elif locally_or_remotely == 'wsl':
        repo_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/"
        repo_result_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/07_PyResults/"
        repo_figure_location = "/mnt/d/OneDrive - Kyushu University/15_Article/03_RStudio/04_Figure/"
    return repo_location, repo_result_location, repo_figure_location

def drawImportanceBar(figure_name):
    importance_lsoverall = load(REPO_RESULT_LOCATION + "98_LSoverall_RfImportance.joblib")
    importance_lsrelative = load(REPO_RESULT_LOCATION + "98_LSrelative_RfImportance.joblib")
    importance_happinessoverall = load(REPO_RESULT_LOCATION + "98_Happinessoverall_RfImportance.joblib")
    importance_happinessrelative = load(REPO_RESULT_LOCATION + "98_Happinessrelative_RfImportance.joblib")
    
    feature_name = ["Year", "Latitude", "Longitude", "Female Dummy", "Age", 
                    "High-level Stress", "Low-level Stress", "Easy to Relax",
                    "Goodness for Living", "Living Environment Safety", 
                    "Community Attachment", "Income Level", "Self-Reported Health", 
                    "Student Dummy", "Worker Dummy", "Company Owner Dummy",
                    "Government Officer Dummy", "Self Employed Dummy",
                    "Professional Dummy", "Housewife Dummy", "Retired Dummy",
                    "Unemployed Dummy", "College No Diploma Dummy",
                    "Bachelor Dummy", "Master Dummy", "PhD Dummy", 
                    "Individual Income", "NDVI", "NTL"]
    y_pos = np.arange(len(feature_name))
    
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(24, 16), dpi=300,
                            constrained_layout=True)
    axs[0,0].barh(y_pos, importance_lsoverall.importances_mean, 
                  xerr=importance_lsoverall.importances_std*1.96, align='center',
                  color = 'blue', edgecolor='black')
    axs[0,0].set_yticks(y_pos, labels=feature_name)
    axs[0,0].invert_yaxis() 
    axs[0,0].set_xlabel('Permutation Importance', fontsize=14)
    axs[0,0].tick_params(axis='both', which='major', labelsize=14)
    axs[0,0].grid(linestyle='dashed')
    axs[0,0].set_xlabel("OVLS", fontsize=15, fontweight='bold')
    axs[0,0].set_ylim([29, -1])
    
    axs[0,1].barh(y_pos, importance_lsrelative.importances_mean, 
                  xerr=importance_lsrelative.importances_std*1.96, align='center',
                  color = 'orange', edgecolor='black')
    axs[0,1].set_yticks(y_pos, labels=feature_name)
    axs[0,1].invert_yaxis() 
    axs[0,1].set_xlabel('Permutation Importance', fontsize=14)
    axs[0,1].tick_params(axis='both', which='major', labelsize=14)
    axs[0,1].grid(linestyle='dashed')
    axs[0,1].set_xlabel("RLS", fontsize=15, fontweight='bold')
    axs[0,1].set_ylim([29, -1])
    
    axs[1,0].barh(y_pos, importance_happinessoverall.importances_mean, 
                  xerr=importance_happinessoverall.importances_std*1.96, align='center',
                  color = 'green', edgecolor='black')
    axs[1,0].set_yticks(y_pos, labels=feature_name)
    axs[1,0].invert_yaxis() 
    axs[1,0].set_xlabel('Permutation Importance', fontsize=14)
    axs[1,0].tick_params(axis='both', which='major', labelsize=14)
    axs[1,0].grid(linestyle='dashed')
    axs[1,0].set_xlabel("OH", fontsize=15, fontweight='bold')
    axs[1,0].set_ylim([29, -1])
    
    axs[1,1].barh(y_pos, importance_happinessrelative.importances_mean, 
                  xerr=importance_happinessrelative.importances_std*1.96, align='center',
                  color = 'red', edgecolor='black')
    axs[1,1].set_yticks(y_pos, labels=feature_name)
    axs[1,1].invert_yaxis() 
    axs[1,1].set_xlabel('Permutation Importance', fontsize=14)
    axs[1,1].tick_params(axis='both', which='major', labelsize=14)
    axs[1,1].grid(linestyle='dashed')
    axs[1,1].set_xlabel("RH", fontsize=15, fontweight='bold')
    axs[1,1].set_ylim([29, -1])
    
    
    plt.savefig(REPO_FIGURE_LOCATION + figure_name, bbox_inches='tight')
    return None

REPO_LOCATION, REPO_RESULT_LOCATION, REPO_FIGURE_LOCATION = runLocallyOrRemotely(Locally_Or_Remotely = "y")

drawImportanceBar("importance.jpg")
