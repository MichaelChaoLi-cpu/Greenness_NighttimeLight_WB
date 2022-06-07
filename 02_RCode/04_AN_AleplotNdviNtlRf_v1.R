# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(DALEX)
library(doSNOW)
library(ALEPlot)
library(tcltk)
library(pdp)

findBestFitFunction <- function(input_pdp, highest_order = 20, decide_value = 0.99, weights = NULL){
  if (!is.null(weights)){
    if(!(nrow(input_pdp)==length(weights))){stop("Weights have a different length with input data!")}
  }
  input_pdp <- input_pdp %>% as.matrix() %>% as.data.frame()
  input_pdp <- input_pdp %>% dplyr::select('yhat', dplyr::everything())
  y <- input_pdp %>% dplyr::select('yhat')
  x <- input_pdp %>% dplyr::select(-'yhat')
  for (order in seq(1,highest_order)){
    x[,paste0("order_", as.character(order))] <- input_pdp[,2]^order
  }
  x <- x[2:ncol(x)]
  r2_array <- c()
  first_time <- T
  if(is.null(weights)){cat('Unweighted!\n')} else{
    cat('Weighted!\n')
  }
  for (order in seq(1,highest_order)){
    data <- cbind(y, x[1:order])
    
    if(is.null(weights)) {
      regression <- lm(yhat ~ ., data)
      r2 <- summary(regression)$adj.r.squared
    } else {
      regression <- lm(yhat ~ ., data, weights = weights)
      r2 <- summary(regression)$adj.r.squared
    }
    if((r2>decide_value)&(first_time == T)){
      first_over_decide_value <- order
      keep.model <- regression
      first_time <- F
    }
    r2_array <- append(r2_array, r2)
  }
  if(first_time == T){
    first_over_decide_value <- NULL
    keep.model <- regression
  }
  cat(first_over_decide_value)
  result <- list(first_over_decide_value, r2_array, keep.model)
  return(result)
}

predictPDP <- function(input_pdp, decided_order = 20, weights_vector = NULL){
  if (is.null(decided_order)) {decided_order = 20}
  cat("decide order: ", decided_order)
  input_pdp <- input_pdp %>% as.matrix() %>% as.data.frame()
  input_pdp <- input_pdp %>% dplyr::select('yhat', dplyr::everything())
  y <- input_pdp %>% dplyr::select('yhat')
  x <- input_pdp %>% dplyr::select(-'yhat')
  for (order in seq(1,decided_order)){
    x[,paste0("order_", as.character(order))] <- input_pdp[,2]^order
  }
  x <- x[2:ncol(x)]
  data <- cbind(y, x)
  regression <- lm(yhat ~., data = data, weights = weights_vector)
  input_pdp$yhat_pred <- predict(regression, data)
  output_list <- list(input_pdp, regression)
  return(output_list)
}

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

ALE.2.rf24.NDVI.only = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat,
                               J = c('NDVI'), K = 500, NA.plot = T)

ALE.2.rf24.NTL.only = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat,
                               J = c('NTL_log'), K = 500, NA.plot = T)

ALE.2.rf24.income.only = ALEPlot(dataset_used.rf[,2:25], data.rf.24, pred.fun = yhat,
                                 J = c('income_indiv'), K = 500, NA.plot = T)
run <- F
if(run){
  save(ALE.2.rf24.NDVI.only, ALE.2.rf24.NTL.only, ALE.2.rf24.income.only,
       file = "03_Results/06_ALE.2.rf24.NDVI.NTL.only.500.RData")
} else {
  load("03_Results/06_ALE.2.rf24.NDVI.NTL.only.500.RData") 
}

#here i think this is unnecessary to get a continuous function here. // we still need
run <- T
if(run){
  ALE.NDVI.only.result <- cbind(ALE.2.rf24.NDVI.only$x.values, ALE.2.rf24.NDVI.only$f.values) %>%
    as.data.frame()
  colnames(ALE.NDVI.only.result) <- c("NDVI", "yhat")
  ALE.NDVI.only.pseudoFunction <- findBestFitFunction(ALE.NDVI.only.result, 12, 0.99, weights = NULL)
  
  pred.ALE.NDVI.only <- predictPDP(input_pdp = ALE.NDVI.only.result, decided_order = 12)
  ggplot(pred.ALE.NDVI.only[[1]], aes(x = NDVI)) +
    geom_point(aes(y = yhat, color = "yhat")) +
    geom_point(aes(y = yhat_pred, color = "yhat_pred")) +
    theme_bw()
  
  ALE.NTL.only.result <- cbind(ALE.2.rf24.NTL.only$x.values, ALE.2.rf24.NTL.only$f.values) %>%
    as.data.frame()
  colnames(ALE.NTL.only.result) <- c("NTL", "yhat")
  ALE.NTL.only.pseudoFunction <- findBestFitFunction(ALE.NTL.only.result, 20, 0.99, weights = NULL)
  
  pred.ALE.NTL.only <- predictPDP(input_pdp = ALE.NTL.only.result, decided_order = 2)
  ggplot(pred.ALE.NTL.only[[1]], aes(x = NTL)) +
    geom_point(aes(y = yhat, color = "yhat")) +
    geom_point(aes(y = yhat_pred, color = "yhat_pred")) +
    theme_bw()
  
  ALE.income.only.result <- cbind(ALE.2.rf24.income.only$x.values, ALE.2.rf24.income.only$f.values) %>%
    as.data.frame()
  colnames(ALE.income.only.result) <- c("income", "yhat")
  ALE.NTL.only.pseudoFunction <- findBestFitFunction(ALE.income.only.result, 20, 0.99, weights = NULL)
  
  pred.ALE.income.only <- predictPDP(input_pdp = ALE.income.only.result, decided_order = 6)
  ggplot(pred.ALE.income.only[[1]], aes(x = income)) +
    geom_point(aes(y = yhat, color = "yhat")) +
    geom_point(aes(y = yhat_pred, color = "yhat_pred")) +
    theme_bw()
}

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
} else {
  load("03_Results/03_data.rf.24.PDP.NDVI.RData")
}

ALE.NDVI.only.pseudoFunction <- findBestFitFunction(ALE.NDVI.only.result, 12, 0.99, weights = NULL)
ALE.NDVI.pseudo.coeff <- ALE.NDVI.only.pseudoFunction[[3]] %>% coefficients() %>% as.numeric()
ME.estimation.dataset.used <- dataset_used.rf %>%
  mutate(ME.NDVI = ALE.NDVI.pseudo.coeff[2] + ALE.NDVI.pseudo.coeff[3] * NDVI + 
           ALE.NDVI.pseudo.coeff[4] * NDVI^2 + ALE.NDVI.pseudo.coeff[5] * NDVI^3 +
           ALE.NDVI.pseudo.coeff[6] * NDVI^4 + ALE.NDVI.pseudo.coeff[7] * NDVI^5 +
           ALE.NDVI.pseudo.coeff[8] * NDVI^6 + ALE.NDVI.pseudo.coeff[9] * NDVI^7 +
           ALE.NDVI.pseudo.coeff[10] * NDVI^8 + ALE.NDVI.pseudo.coeff[11] * NDVI^9 + 
           ALE.NDVI.pseudo.coeff[12] * NDVI^10 + ALE.NDVI.pseudo.coeff[13] * NDVI^11)

ALE.NTL.only.pseudoFunction <- findBestFitFunction(ALE.NTL.only.result, 2, 0.99, weights = NULL)
ALE.NTL.pseudo.coeff <- ALE.NTL.only.pseudoFunction[[3]] %>% coefficients() %>% as.numeric()
ME.estimation.dataset.used <- ME.estimation.dataset.used %>%
  mutate(ME.NTL = (ALE.NTL.pseudo.coeff[2] + ALE.NTL.pseudo.coeff[3] * NTL_log)/exp(NTL_log) )

ALE.income.only.pseudoFunction <- findBestFitFunction(ALE.income.only.result, 6, 0.99, weights = NULL)
ALE.income.pseudo.coeff <- ALE.income.only.pseudoFunction[[3]] %>% coefficients() %>% as.numeric()
ME.estimation.dataset.used <- ME.estimation.dataset.used %>%
  mutate(ME.income = ALE.income.pseudo.coeff[2] + ALE.income.pseudo.coeff[3] * income_indiv + 
           ALE.income.pseudo.coeff[4] * income_indiv^2 + ALE.income.pseudo.coeff[5] * income_indiv^3 +
           ALE.income.pseudo.coeff[6] * income_indiv^4 + ALE.income.pseudo.coeff[7] * income_indiv^5)

ME.estimation.dataset.used <- ME.estimation.dataset.used %>%
  mutate(MRS.NDVI = ME.NDVI/ME.income,
         MRS.NTL = ME.NTL/ME.income)
save(ME.estimation.dataset.used, file = "03_Results/07_MRS.result.NDVI.NTL.RData", version = 2)
