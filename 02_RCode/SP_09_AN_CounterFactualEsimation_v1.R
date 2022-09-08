# Author: M.L.

# Aim: this script is to calculation monetary value of counterfactual
# on HPC

# end

library(randomForest)
library(tidyverse)
library(dplyr)
library(foreach)
library(doParallel)
library(doSNOW)

source("DP15/02_RCode/SP_07_AF_CounterFactualCalibrationForIncome_v1.R")

load("DP15/01_Data/07_dataset.rf26.RData")
load("DP15/03_Results/11_data.rf.26.SP.RData")
X <- dataPre(dataset_used.rf.26)

notHave <- T
if(notHave){
  counterfactualValueOfNDVIforIncomeChange1 <-
    aggregateCounterfactual(X, data.rf.26, "income_indiv",marginalChange = 1,
                            0.01, "NDVI", 5, 5*10^-3, 3)
  save(counterfactualValueOfNDVIforIncomeChange1, file = "DP15/03_Results/97_temp_NDVICounterfactualValue.Rdata")
}

notHave <- F
if(notHave){
  counterfactualValueOfNTLforIncomeChange1 <-
    aggregateCounterfactual(X, data.rf.26, "income_indiv",marginalChange = 1,
                            0.01, "NTL_log", 1, 10^-3, 3)
  save(counterfactualValueOfNTLforIncomeChange1, file = "DP15/03_Results/97_temp_NTLCounterfactualValue.Rdata")
}

#counterfactualValueOfNDVIforIncomeChange1 <-
#  aggregateCounterfactual(X[1:100,], data.rf.26, "income_indiv",marginalChange = 1,
#                          0.01, "NDVI", 5, 10^-3, 4)