# Author: M.L.

# end


library(foreach)
library(randomForest)
library(tidyverse)
library(doSNOW)
library(pdp)


load("DP15/01_Data/06_dataset.rf24.RData")

#data.rf.24 <- randomForest(overall_LS ~., data = dataset_used.rf, na.action = na.omit, ntree = 1000, 
#                           importance = T, mtry = 8)
### since the there is 24 predictors, we select 24/3 ~ 8

# do SNOW
cl <- makeSOCKcluster(100)
registerDoSNOW(cl)
getDoParWorkers()

ntasks <- 10

data.rf.24 <- 
  foreach(ntree = rep(100, ntasks), .combine = randomForest::combine,
          .multicombine=TRUE, .packages='randomForest') %dopar% {
            randomForest(overall_LS ~., data = dataset_used.rf, 
                         na.action = na.omit, ntree = ntree,
                         importance = T, mtry = 8)
          }
stopCluster(cl)
# do SNOW

cat("Here, we are")

save(data.rf.24, file = "DP15/03_Results/00_data.rf.24.SP.RData", version = 2)

cat("Pass")
