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
# y_inc with orderID
rfPredictYchangeFeature <- function(dataRF, modelRF, incomeName, marginalChange){
  dataRF[,incomeName] <- dataRF[,incomeName] + marginalChange
  y_inc = predict(modelRF, newdata = dataRF)
  df <- cbind(seq(1, length(y_inc), 1), y_inc)
  colnames(df) <- c("orderID", "y_inc")
  return(df)
}

### this function find the reasonable FOI value to satisfy the counterfactural of income change
multiCounterfactual <- function(singleDataRF, modelRF, aimY, tolerance, foiName,
                                foiChangeLimit, foiAccuracy, i){
  i <- i - 1
  positiveIncreaseFoiValue <- foiChangeLimit/foiAccuracy * i
  rawDF <- singleDataRF
  ### Positive
  singleDataRF <- rawDF
  singleDataRF[,foiName] <- singleDataRF[,foiName] + positiveIncreaseFoiValue
  y_inc_new <- predict(modelRF, newdata = singleDataRF)
  aimY_pos <- as.data.frame(cbind(aimY, y_inc_new))
  aimY_pos$yes <- ifelse(abs(aimY_pos$y_inc - aimY_pos$y_inc_new) < tolerance, 1, 0)
  aimY_pos <- aimY_pos[aimY_pos$yes == 1,]
  aimY_pos <- aimY_pos["orderID"]
  aimY_pos$incValue <- i
  aimY_pos$pos <- 1
  
  ### Negative
  singleDataRF <- rawDF
  singleDataRF[,foiName] <- singleDataRF[,foiName] - positiveIncreaseFoiValue
  y_inc_new <- predict(modelRF, newdata = singleDataRF)
  aimY_neg <- as.data.frame(cbind(aimY, y_inc_new))
  aimY_neg$yes <- ifelse(abs(aimY_neg$y_inc - aimY_neg$y_inc_new) < tolerance, 1, 0)
  aimY_neg <- aimY_neg[aimY_neg$yes == 1,]
  aimY_neg <- aimY_neg["orderID"]
  aimY_neg$incValue <- i
  aimY_neg$pos <- -1
  
  output <- rbind(aimY_pos, aimY_neg)
  return(output)
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
  clusterExport(cl, "multiCounterfactual")
  registerDoSNOW(cl)
  opts <- list(progress=progress_fun)
  df.ouput <-
    foreach(i = seq(1,foiChangeLimit/foiAccuracy, 1), .combine = 'rbind', 
            .packages=c('randomForest'), .options.snow=opts) %dopar% {
              multiCounterfactual(dataRF, modelRF, y_inc, tolerance, 
                                  foiName, foiChangeLimit, foiAccuracy, i)
            }
  stopCluster(cl)
  return(df.ouput)
}
