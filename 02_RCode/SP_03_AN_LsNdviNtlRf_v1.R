# Author: M.L.

# input: 07_dataset.rf26.RData
# 07_dataset.rf26.RData: "ID", the respondent id,
#                        "post_code", this is postal code of respondents.
#                        ...
#                        "overall_LS", output variable.
#                        "age", "high_stress", "low_stress", "easy_to_relax"
#                        "good_for_living", "live_environment_satefy",
#                        "community_attachment", "self_reported_health",
#                        "female", "student", "worker", "company_owner", 
#                        "government_officer", "self_employed", "professional",
#                        "housewife", "retired", "unemployed",
#                        "college_no_diploma", "bachelor", "master", "phd",
#                        "income_indiv", "NDVI", "NTL" (24 features) 
#                        Compared with 06_dataset.rf24.RData, there are 2 additional
#                        variables:
#                        "lon", "lat"
# Note: this is the clear version data of 04_dataset_used.RData for HPC

# output: 11_data.rf.26.RData
# 11_data.rf.26.RData: the raw random forest model with 1000 trees.

# end

#### Linux ####

#!/bin/bash
#PJM -L "rscunit=ito-a"
#PJM -L "rscgrp=ito-m"
#PJM -L "vnode=1"
#PJM -L "vnode-core=36"
#PJM -L "elapse=24:00:00"
#PJM -j
#PJM -X

##source init.sh

##R --slave --vanilla --args 10 20 < /home/usr6/q70176a/DP15/02_RCode/SP_04_AN_AleplotNdviNtlRf_v1.R


library(foreach)
library(randomForest)
library(tidyverse)
library(doSNOW)
library(pdp)


load("DP15/01_Data/07_dataset.rf26.RData")

#data.rf.24 <- randomForest(overall_LS ~., data = dataset_used.rf, na.action = na.omit, ntree = 1000, 
#                           importance = T, mtry = 8)
### since the there is 24 predictors, we select 24/3 ~ 8

# do SNOW
clusterNumber <- 50
cl <- makeSOCKcluster(clusterNumber)
registerDoSNOW(cl)
getDoParWorkers()

ntasks <- 20

data.rf.26 <- 
  foreach(ntree = rep(clusterNumber, ntasks), .combine = randomForest::combine,
          .multicombine=TRUE, .packages='randomForest') %dopar% {
            randomForest(overall_LS ~., data = dataset_used.rf.26, 
                         na.action = na.omit, ntree = ntree,
                         importance = T, mtry = 9)
          }
stopCluster(cl)
# do SNOW

cat("Here, we are")

save(data.rf.26, file = "DP15/03_Results/11_data.rf.26.SP.RData", version = 2)

cat("Pass")
