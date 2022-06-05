# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(DALEX)
library(doSNOW)
library(ALEPlot)
library(tcltk)
library(pdp)

load("03_Results/00_data.rf.24.RData")
load("01_Data/06_dataset.rf24.RData")
run <- F
if(run){
  ALE.2.rf24 = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat, 
                  J = c('NDVI', 'NTL_log'), K = 100, NA.plot = T)
  image(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, xlab = "NDVI", ylab = "NTL")
  contour(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, add = T, drawlabels = T)
  
  ALE.2.rf24.inc_NTL = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat, 
                       J = c('income_indiv', 'NTL_log'), K = 100, NA.plot = T)
  image(ALE.2.rf24.inc_NTL$x.values[[1]], ALE.2.rf24.inc_NTL$x.values[[2]],
        ALE.2.rf24.inc_NTL$f.values, xlab = "Income", ylab = "NTL")
  contour(ALE.2.rf24.inc_NTL$x.values[[1]], ALE.2.rf24.inc_NTL$x.values[[2]],
          ALE.2.rf24.inc_NTL$f.values, add = T, drawlabels = T)
  
  ALE.2.rf24.inc_NDVI = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat, 
                               J = c('income_indiv', 'NDVI'), K = 100, NA.plot = T)
  image(ALE.2.rf24.inc_NDVI$x.values[[1]], ALE.2.rf24.inc_NDVI$x.values[[2]],
        ALE.2.rf24.inc_NDVI$f.values, xlab = "Income", ylab = "NDVI")
  contour(ALE.2.rf24.inc_NDVI$x.values[[1]], ALE.2.rf24.inc_NDVI$x.values[[2]],
          ALE.2.rf24.inc_NDVI$f.values, add = T, drawlabels = T)
  
  save(ALE.2.rf24, ALE.2.rf24.inc_NTL, ALE.2.rf24.inc_NDVI, file = "03_Results/02_ALE.2.rf24.RData")
}

ALE.2.rf24.NDVI.NTL.500 = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat,
                                  J = c('NDVI', 'NTL_log'), K = 500, NA.plot = T)
save(ALE.2.rf24.NDVI.NTL.500, file = "03_Results/02_ALE.2.rf24.NDVI.NTL.500.RData")


####
# this part is done by supercomputer
run <- F
if(run){
  #### pdp
  cl <- makeSOCKcluster(6)
  registerDoSNOW(cl)
  getDoParWorkers()
  
  pdp.rf24.NDVI <- partial(data.rf.24, pred.var = "NDVI",
                                 grid.resolution = 5000,
                                 plot = F, rug = T, parallel = T,
                                 paropts = list(.packages = "randomForest"))
  
  stopCluster(cl)
  registerDoSNOW()
  
  cl <- makeSOCKcluster(14)
  registerDoSNOW(cl)
  getDoParWorkers()
  
  pdp.rf24.NTL_log <- partial(data.rf.24, pred.var = "NTL_log",
                           grid.resolution = 5000,
                           plot = F, rug = T, parallel = T,
                           paropts = list(.packages = "randomForest"))
  
  stopCluster(cl)
  registerDoSNOW()
}
