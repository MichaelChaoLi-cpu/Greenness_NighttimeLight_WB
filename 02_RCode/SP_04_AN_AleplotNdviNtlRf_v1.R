# Author: M.L.

# input: 06_dataset.rf24.RData
# 06_dataset.rf24.RData: "ID", the respondent id,
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
# Note: this is the clear version data of 04_dataset_used.RData for HPC

# input: 00_data.rf.24.RData
# 00_data.rf.24.RData: the raw random forest model with 1000 trees.

# output: 03_data.rf.24.PDP.NDVI.RData
# 03_data.rf.24.PDP.NDVI.RData: "result", pdp value of NDVI
#                               "V2", NDVI values

# output: 04_data.rf.24.PDP.NTL.RData
# 04_data.rf.24.PDP.NTL.RData: "result", pdp value of NTL
#                              "V2", NTL values

# output: 05_data.rf.24.PDP.income.RData
# 05_data.rf.24.PDP.income.RData: "result", pdp value of income
#                                 "V2", income values

# end

'
#!/bin/bash
#PJM -L "rscunit=ito-a"
#PJM -L "rscgrp=ito-m"
#PJM -L "vnode=8"
#PJM -L "vnode-core=36"
#PJM -L "elapse=24:00:00"
#PJM -j
#PJM -X

source init.sh

R --slave --vanilla --args 10 20 < /home/usr6/q70176a/DP15/02_RCode/SP_04_AN_AleplotNdviNtlRf_v1.R
'

library(foreach)
library(randomForest)
library(tidyverse)
library(doSNOW)
#library(pdp)


### discarded 24  variable
#load("/home/usr6/q70176a/DP15/01_Data/06_dataset.rf24.RData")

load("/home/usr6/q70176a/DP15/01_Data/07_dataset.rf26.RData")

#data.rf.24 <- randomForest(overall_LS ~., data = dataset_used.rf, na.action = na.omit, ntree = 1000, 
#                           importance = T, mtry = 8)
### since the there is 24 predictors, we select 24/3 ~ 8
Sys.time()
cat("Here, Random forest \n")

# do parallel
#run <- F
#if(run){
#  cl <- makeSOCKcluster(100)
#  registerDoSNOW(cl)
#  getDoParWorkers()
#  
#  ntasks <- 10
#  
#  data.rf.24 <- 
#    foreach(ntree = rep(100, ntasks), .combine = randomForest::combine,
#            .multicombine=TRUE, .packages='randomForest') %dopar% {
#              randomForest(overall_LS ~., data = dataset_used.rf, 
#                           na.action = na.omit, ntree = ntree,
#                           importance = T, mtry = 8)
#            }
#  stopCluster(cl)
#  # do SNOW
#  
#  save(data.rf.24, file = "/home/usr6/q70176a/DP15/03_Results/00_data.rf.24.SP.RData", version = 2)
#} else {
#  load("/home/usr6/q70176a/DP15/03_Results/00_data.rf.24.SP.RData")
#  Sys.time()
#}
run <- T
if(run){
  cl <- makeSOCKcluster(125)
  registerDoSNOW(cl)
  getDoParWorkers()
  
  ntasks <- 8
  
  data.rf.26 <- 
    foreach(ntree = rep(125, ntasks), .combine = randomForest::combine,
            .multicombine=TRUE, .packages='randomForest') %dopar% {
              randomForest(overall_LS ~., data = dataset_used.rf.26, 
                           na.action = na.omit, ntree = ntree,
                           importance = T, mtry = 9)
            }
  stopCluster(cl)
  # do SNOW
  
  save(data.rf.26, file = "/home/usr6/q70176a/DP15/03_Results/00_data.rf.26.SP.RData", version = 2)
} else {
  load("/home/usr6/q70176a/DP15/03_Results/00_data.rf.26.SP.RData")
  Sys.time()
}

cat("Here, we have saved the rf model\n")

cat("Here, we are, go to pdp\n")

partialDependcyPlot <- function(dataset_used.rf, data.rf.24, aim.var, aim.value, formula.in){
  test.predict.data <- dataset_used.rf %>% 
    dplyr::select(-all.vars(formula.in)[1]) 
  test.predict.data[aim.var] <- aim.value
  predict.output <- mean(predict(data.rf.24, test.predict.data))
  return(predict.output)
}

run <- F
if(run){
  #### pdp
  gc()
  cl <- makeSOCKcluster(4)
  registerDoSNOW(cl)
  getDoParWorkers()
  progress <- function(n) {
    if(n%%50 == 0){
      cat(sprintf("task %d is complete\n", n)) 
    }
  }
  opts <- list(progress = progress)
  
  result <- 
    foreach(aim.value = seq(4.8, 87.8, 0.1), .combine = append, 
            .packages=c('tidyverse',"randomForest"),
            .options.snow = opts) %dopar% {
              partialDependcyPlot(dataset_used.rf %>% na.omit(), data.rf.24, "NDVI", aim.value, overall_LS ~.)
            }
  stopCluster(cl)
  Sys.time()
  pdp.rf24.NDVI <- as.data.frame(cbind(result, seq(4.8, 87.8, 0.1)))
  save(pdp.rf24.NDVI, file = "/home/usr6/q70176a/DP15/03_Results/03_data.rf.24.PDP.NDVI.RData")
}

#cl <- makeSOCKcluster(4)
#registerDoSNOW(cl)
#getDoParWorkers()
#progress <- function(n) {
#  if(n%%50 == 0){
#    cat(sprintf("task %d is complete\n", n)) 
#  }
#}
#opts <- list(progress = progress)

#Sys.time()
#pdp.rf24.NDVI <- pdp::partial(data.rf.24, pred.var = "NDVI",
#                               grid.resolution = 1000,
#                               plot = F, rug = T, parallel = T,
#                               paropts = list(.packages = "randomForest",
#                                              .options.snow = opts))
#Sys.time()
#
#stopCluster(cl)


cat("Here, we are, go to second pdp\n")

run <- F
if(run){
  #### pdp
  gc()
  cl <- makeSOCKcluster(4)
  registerDoSNOW(cl)
  getDoParWorkers()
  progress <- function(n) {
    if(n%%50 == 0){
      cat(sprintf("task %d is complete\n", n)) 
    }
  }
  opts <- list(progress = progress)
  
  result <- 
    foreach(aim.value = seq(0.01, 4.50, 0.01), .combine = append, 
            .packages=c('tidyverse',"randomForest"),
            .options.snow = opts) %dopar% {
              partialDependcyPlot(dataset_used.rf %>% na.omit(), data.rf.24, "NTL_log", aim.value, overall_LS ~.)
            }
  stopCluster(cl)
  pdp.rf24.NTL_log <- as.data.frame(cbind(result, seq(0.01, 4.50, 0.01)))
  Sys.time()
  save(pdp.rf24.NTL_log, file = "/home/usr6/q70176a/DP15/03_Results/04_data.rf.24.PDP.NTL.RData")
}
#cl <- makeSOCKcluster(10)
#registerDoSNOW(cl)
#getDoParWorkers()
#progress <- function(n) {
#  if(n%%50 == 0){
#    cat(sprintf("task %d is complete\n", n)) 
#  }
#}
#opts <- list(progress = progress)

#Sys.time()
#pdp.rf24.NTL_log <- pdp::partial(data.rf.24, pred.var = "NTL_log",
#                         grid.resolution = 1000,
#                         plot = F, rug = T, parallel = T,
#                         paropts = list(.packages = "randomForest",
#                                        .options.snow = opts))
#Sys.time()

#stopCluster(cl)
#save(pdp.rf24.NDVI, file = "/home/usr6/q70176a/DP15/03_Results/04_data.rf.24.PDP.NTL.RData")

cat("Here, we are, go to third pdp\n")

run <- F
if(run){
  #### pdp
  gc()
  cl <- makeSOCKcluster(4)
  registerDoSNOW(cl)
  getDoParWorkers()
  progress <- function(n) {
    if(n%%50 == 0){
      cat(sprintf("task %d is complete\n", n)) 
    }
  }
  opts <- list(progress = progress)
  
  result <- 
    foreach(aim.value = dataset_used.rf$income_indiv %>% unique() %>% sort(), .combine = append, 
            .packages=c('tidyverse',"randomForest"),
            .options.snow = opts) %dopar% {
              partialDependcyPlot(dataset_used.rf %>% na.omit(), data.rf.24, "income_indiv", aim.value, overall_LS ~.)
            }
  stopCluster(cl)
  pdp.rf24.NTL_log <- as.data.frame(cbind(result, dataset_used.rf$income_indiv %>% unique() %>% sort()))
  Sys.time()
  save(pdp.rf24.NTL_log, file = "/home/usr6/q70176a/DP15/03_Results/05_data.rf.24.PDP.income.RData")
}

cat("Here, done\n")