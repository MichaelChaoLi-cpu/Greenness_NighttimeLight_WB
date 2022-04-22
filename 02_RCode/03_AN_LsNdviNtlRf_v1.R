# Author: M.L.

# end

library(ggplot2)
library(cowplot)
library(foreach)
library(randomForest)
library(tidyverse)
library(DALEX)
library(doSNOW)
library(tcltk)
library(pdp)

load("01_Data/04_dataset_used.RData")
dataset_used <- dataset_used %>%
  mutate(live_environment_satefy = ifelse(live_environment_satefy==0, NA, live_environment_satefy))
dataset_used <- dataset_used %>%
  mutate(NTL_log = ifelse(NTL < 0, 0, NTL))
dataset_used$NTL_log <- log(dataset_used$NTL_log + 1)
dataset_used$NTL_log %>% hist()
hist(dataset_used$NDVI)

formula_LS <- overall_LS ~ live_environment_satefy + 
  good_for_living + community_attachment + high_stress + low_stress +
  female + age + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd +  NDVI + NTL_log

dataset_used.rf <- dataset_used %>% dplyr::select(all.vars(formula_LS), student:unemployed) %>% na.omit()


#data.rf.24 <- randomForest(overall_LS ~., data = dataset_used.rf, na.action = na.omit, ntree = 1000, 
#                           importance = T, mtry = 8)
### since the there is 24 predictors, we select 24/3 ~ 8

# do SNOW
cl <- makeSOCKcluster(15)
registerDoSNOW(cl)

ntasks <- 100
pb <- tkProgressBar(max=ntasks)
progress <- function(n) setTkProgressBar(pb, n)
opts <- list(progress=progress)

data.rf.24 <- 
  foreach(ntree = rep(10, ntasks), .combine = randomForest::combine,
          .multicombine=TRUE, .packages='randomForest',
          .options.snow=opts) %dopar% {
            randomForest(overall_LS ~., data = dataset_used.rf, 
                         na.action = na.omit, ntree = ntree,
                         importance = T, mtry = 8)
          }
stopCluster(cl)
# do SNOW

save(data.rf.24, file = "03_Results/00_data.rf.24.RData", version = 2)

plot(data.rf.24)
importance(data.rf.24)
varImpPlot(data.rf.24)
print(data.rf.24)

### calculate loss function
loss_root_mean_square(dataset_used.rf$overall_LS, yhat(data.rf.24, dataset_used.rf))

### unified the model
explainer_data.rf.24 = explain(data.rf.24, data = dataset_used.rf, y = dataset_used.rf$overall_LS)
diag_data.rf.24 <- model_diagnostics(explainer_data.rf.24)
plot(diag_data.rf.24)
plot(diag_data.rf.24, variable = "y", yvariable = "residuals")
hist(dataset_used.rf$overall_LS, breaks = rep(0:5, 1))

### model information
model_info(data.rf.24)

### Dataset Level Variable Importance as Change in Loss Function after Variable Permutations
data.rf.24_aps <- model_parts(explainer_data.rf.24, type = "raw")
head(data.rf.24_aps, 10)
plot(data.rf.24_aps)

### model performance
model_performance_data.rf.24 <- model_performance(explainer_data.rf.24)
model_performance_data.rf.24
plot(model_performance_data.rf.24)

lm(overall_LS ~., data = dataset_used.rf) %>% summary()

### test the line
### Dataset Level Variable Profile as Partial Dependence or Accumulated Local Dependence Explanations
model_profile_data.rf.24 <- model_profile(explainer_data.rf.24)
plot(model_profile_data.rf.24, variables = "NDVI")
plot(model_profile_data.rf.24, variables = "NTL_log")
plot(model_profile_data.rf.24, variables = "income_indiv")
