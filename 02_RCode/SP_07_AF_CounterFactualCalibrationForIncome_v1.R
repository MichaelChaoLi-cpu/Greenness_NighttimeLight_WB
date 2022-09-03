# Author: M.L.

# Aim: this script is to calculation monetary value of counterfactual

# end

library(randomForest)
library(tidyverse)
library(dplyr)
library(foreach)
library(doParallel)
library(doSNOW)

dataPre <- function(data){
  X <- data %>% dplyr::select(-overall_LS)
  return(X)
}

### this function is to increase 1-unit income
# since the income in this research is discrete.
rfPredictYchangeFeature <- function(dataRF, modelRF, incomeName, marginalChange){
  dataRF[,incomeName] <- dataRF[,incomeName] + marginalChange
  y_inc = predict(modelRF, newdata = dataRF)
  return(y_inc)
}

### this function find the reasonable FOI value to satisfy the counterfactural of income change
singleCounterfactual <- function(singleDataRF, modelRF, aimY, tolerance, foiName,
                                 foiChangeLimit, foiAccuracy){
  lineNumber <- foiChangeLimit/foiAccuracy * 2 + 1
  halfLineNumber <- foiChangeLimit/foiAccuracy
  searchingDataRF <- singleDataRF[rep(1, lineNumber),]
  changeValue <- seq(-foiChangeLimit, foiChangeLimit, foiAccuracy)
  searchingDataRF[,foiName] <- searchingDataRF[,foiName] + changeValue
  y_inc = predict(modelRF, newdata = searchingDataRF)
  yChange <- abs(y_inc - aimY)
  resultTable <- as.data.frame(cbind(seq(-halfLineNumber, halfLineNumber, 1), yChange))
  resultTable <- resultTable[resultTable$yChange<0.1,]
  if(nrow(resultTable) > 0){
    resultTable$direction <- resultTable[,1]/abs(resultTable[,1])
    resultTable[is.na(resultTable[,3]),3] <- 1
    resultTable[,1] <- abs(resultTable[,1])
    direction <- resultTable[resultTable[,1]==min(resultTable[,1]),3]
    returnValue <- min(resultTable[,1]) * direction * foiAccuracy
    if(length(returnValue)>1){
      returnValue <- returnValue[1]
    }
  } else {
    returnValue <- NA
  }
  return(returnValue)
}

progress_fun <- function(n){
  cat(n, ' ')
  if (n%%100==0){
    cat('\n')
  }
}

# parallel running the singleCounterfactual
aggregateCounterfactual <- function(dataRF, modelRF, incomeName, marginalChange, 
                                    tolerance, foiName, foiChangeLimit, 
                                    foiAccuracy, clusterNumber){
  y_inc <- rfPredictYchangeFeature(dataRF, modelRF, incomeName, marginalChange)
  cl <- makeSOCKcluster(clusterNumber)
  clusterExport(cl, "singleCounterfactual")
  registerDoSNOW(cl)
  opts <- list(progress=progress_fun)
  df.ouput <-
    foreach(i = seq(1,nrow(dataRF), 1), .combine = 'c', 
            .packages='randomForest', .options.snow=opts) %dopar% {
              singleCounterfactual(dataRF[i,], modelRF, y_inc[i], tolerance, 
                                   foiName, foiChangeLimit, foiAccuracy)
            }
  stopCluster(cl)
  return(df.ouput)
}
