# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(doSNOW)
library(pdp)

load("DP15/03_Results/00_data.rf.24.RData")
load("DP15/01_Data/06_dataset.rf24.RData")

#### pdp
cl <- makeSOCKcluster(36)
registerDoSNOW(cl)
getDoParWorkers()

pdp.rf24.NDVI <- partial(data.rf.24, pred.var = "NDVI",
                               grid.resolution = 5000,
                               plot = F, rug = T, parallel = T,
                               paropts = list(.packages = "randomForest"))

stopCluster(cl)
save(pdp.rf24.NDVI, file = "DP15/03_Results/03_data.rf.24.PDP.NDVI.RData")

cl <- makeSOCKcluster(36)
registerDoSNOW(cl)
getDoParWorkers()

pdp.rf24.NTL_log <- partial(data.rf.24, pred.var = "NTL_log",
                         grid.resolution = 5000,
                         plot = F, rug = T, parallel = T,
                         paropts = list(.packages = "randomForest"))

stopCluster(cl)
save(pdp.rf24.NDVI, file = "DP15/03_Results/04_data.rf.24.PDP.NTL.RData")

