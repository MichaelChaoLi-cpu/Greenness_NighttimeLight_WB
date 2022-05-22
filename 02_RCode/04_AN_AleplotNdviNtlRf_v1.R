# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(DALEX)
library(doSNOW)
library(ALEPlot)

load("03_Results/00_data.rf.24.RData")
load("01_Data/06_dataset,rf24.RData")
ALE.2.rf24 = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat, 
                J = c('NDVI', 'NTL_log'), K = 100, NA.plot = T)
image(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, xlab = "NDVI", ylab = "NTL")
contour(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, add = T, drawlabels = T)
save(ALE.2.rf24, file = "03_Results/02_ALE.2.rf24.RData")
