# Author: M.L.

# end

library(foreach)
library(randomForest)
library(tidyverse)
library(doSNOW)
library(pdp)



load("/home/usr6/q70176a/DP15/01_Data/06_dataset.rf24.RData")

#data.rf.24 <- randomForest(overall_LS ~., data = dataset_used.rf, na.action = na.omit, ntree = 1000, 
#                           importance = T, mtry = 8)
### since the there is 24 predictors, we select 24/3 ~ 8
Sys.time()
cat("Here, Random forest \n")

# do parallel
run <- F
if(run){
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
  
  save(data.rf.24, file = "/home/usr6/q70176a/DP15/03_Results/00_data.rf.24.SP.RData", version = 2)
} else {
  load("/home/usr6/q70176a/DP15/03_Results/00_data.rf.24.SP.RData")
  Sys.time()
}
cat("Here, we have saved the rf model\n")

cat("Here, we are, go to pdp\n")

#### pdp
cl <- makeSOCKcluster(36)
registerDoSNOW(cl)
getDoParWorkers()
progress <- function(n) {
  if(n%%50 == 0){
    cat(sprintf("task %d is complete\n", n)) 
  }
}
opts <- list(progress = progress)

Sys.time()
pdp.rf24.NDVI <- pdp::partial(data.rf.24, pred.var = "NDVI",
                               grid.resolution = 1000,
                               plot = F, rug = T, parallel = T,
                               paropts = list(.packages = "randomForest",
                                              .options.snow = opts))
Sys.time()

stopCluster(cl)
save(pdp.rf24.NDVI, file = "/home/usr6/q70176a/DP15/03_Results/03_data.rf.24.PDP.NDVI.RData")

cat("Here, we are, go to second pdp\n")

cl <- makeSOCKcluster(36)
registerDoSNOW(cl)
getDoParWorkers()
progress <- function(n) {
  if(n%%50 == 0){
    cat(sprintf("task %d is complete\n", n)) 
  }
}
opts <- list(progress = progress)

Sys.time()
pdp.rf24.NTL_log <- pdp::partial(data.rf.24, pred.var = "NTL_log",
                         grid.resolution = 1000,
                         plot = F, rug = T, parallel = T,
                         paropts = list(.packages = "randomForest",
                                        .options.snow = opts))
Sys.time()

stopCluster(cl)
save(pdp.rf24.NDVI, file = "/home/usr6/q70176a/DP15/03_Results/04_data.rf.24.PDP.NTL.RData")

cat("Here, done\n")