# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(ALEPlot)
library(plotly)
library(ggplot2)

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
load("03_Results/02_ALE.2.rf24.RData")

cor.table <- cor(dataset_used.rf)

cor.test(dataset_used.rf$NDVI, dataset_used.rf$NTL_log)
### NDVI NTL
image(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, xlab = "NDVI", ylab = "NTL")
contour(ALE.2.rf24$x.values[[1]], ALE.2.rf24$x.values[[2]], ALE.2.rf24$f.values, add = T, drawlabels = T)

cor.test(dataset_used.rf$income_indiv, dataset_used.rf$NTL_log)
### NTL Income
image(ALE.2.rf24.inc_NTL$x.values[[1]], ALE.2.rf24.inc_NTL$x.values[[2]],
      ALE.2.rf24.inc_NTL$f.values, xlab = "Income", ylab = "NTL")
contour(ALE.2.rf24.inc_NTL$x.values[[1]], ALE.2.rf24.inc_NTL$x.values[[2]],
        ALE.2.rf24.inc_NTL$f.values, add = T, drawlabels = T)

cor.test(dataset_used.rf$income_indiv, dataset_used.rf$NTL_log)
### NDVI Income
image(ALE.2.rf24.inc_NDVI$x.values[[1]], ALE.2.rf24.inc_NDVI$x.values[[2]],
      ALE.2.rf24.inc_NDVI$f.values,xlab = "Income", ylab = "NDVI")
contour(ALE.2.rf24.inc_NDVI$x.values[[1]], ALE.2.rf24.inc_NDVI$x.values[[2]],
        ALE.2.rf24.inc_NDVI$f.values, add = T, drawlabels = T)

load("03_Results/02_ALE.2.rf24.NDVI.NTL.500.RData")
### NDVI NTL
image(ALE.2.rf24.NDVI.NTL.500$x.values[[1]], ALE.2.rf24.NDVI.NTL.500$x.values[[2]],
      ALE.2.rf24.NDVI.NTL.500$f.values, xlab = "NDVI", ylab = "NTL")
contour(ALE.2.rf24.NDVI.NTL.500$x.values[[1]], ALE.2.rf24.NDVI.NTL.500$x.values[[2]],
        ALE.2.rf24.NDVI.NTL.500$f.values, add = T, drawlabels = T)

x.matrix <- as.matrix(ALE.2.rf24.NDVI.NTL.500$x.values[[1]]) %>% t()
rows <- rep(1, 501)
x.matrix <- x.matrix[rows,]

y.matrix <- as.matrix(ALE.2.rf24.NDVI.NTL.500$x.values[[2]])
cols <- rep(1, 501)
y.matrix <- y.matrix[,cols]

z.matrix <- ALE.2.rf24.NDVI.NTL.500$f.values %>% as.matrix()

x.vector <- as.vector(x.matrix)
y.vector <- as.vector(y.matrix)
z.vector <- as.vector(z.matrix)

ale.dataframe <- cbind(x.vector, y.vector, z.vector) %>% as.data.frame()
rm(x.vector, y.vector, z.vector)
colnames(ale.dataframe) <- c("NDVI", "NTL", "LS")

p <- plot_ly(x = ALE.2.rf24.NDVI.NTL.500$x.values[[1]], y = ALE.2.rf24.NDVI.NTL.500$x.values[[2]],
             z = ALE.2.rf24.NDVI.NTL.500$f.values,
             type = "surface")
p

NDVI.line <- 
  ggplot(ale.dataframe, aes(x = NDVI, y = LS, group = NTL)) +
  geom_line(alpha = 0.05, size = 0.5) +
  theme_bw()
jpeg(file="04_Figure/02_NDVI.line.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NDVI.line
dev.off()

NDVI.point <- 
  ggplot(ale.dataframe, aes(x = NDVI, y = LS)) +
  geom_point(alpha = 0.5, shape = 16, color = "grey70", size  = 0.5) +
  geom_smooth() +
  theme_bw()
jpeg(file="04_Figure/03_NDVI.point.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NDVI.point
dev.off()

NTL.line <- 
  ggplot(ale.dataframe, aes(x = NTL, y = LS, group = NDVI)) +
  geom_line(alpha = 0.05, size = 0.5) +
  theme_bw()
jpeg(file="04_Figure/04_NTL.line.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NTL.line
dev.off()

NTL.point <- 
  ggplot(ale.dataframe, aes(x = NTL, y = LS)) +
  geom_point(alpha = 0.5, shape = 16, color = "grey70", size  = 0.5) +
  geom_smooth() +
  theme_bw()
jpeg(file="04_Figure/05_NTL.point.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NTL.point
dev.off()
  
#####
load("03_Results/03_data.rf.24.PDP.NDVI.RData")
(NDVI.line.pdp <- 
  ggplot(pdp.rf24.NDVI, aes(x = V2, y = result)) +
  geom_line(alpha = 0.9, color = "red", size  = 0.5))
  
load("03_Results/04_data.rf.24.PDP.NTL.RData")
(NTL.line.pdp <- 
    ggplot(pdp.rf24.NTL_log, aes(x = V2, y = result)) +
    geom_line(alpha = 0.9, color = "red", size  = 0.5))
