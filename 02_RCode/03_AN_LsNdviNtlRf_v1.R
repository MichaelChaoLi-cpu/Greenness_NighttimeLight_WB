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
cl <- makeSOCKcluster(14)
registerDoSNOW(cl)

ntasks <- 100
pb <- tkProgressBar(max=ntasks)
progress <- function(n) setTkProgressBar(pb, n)
opts <- list(progress=progress)

data.rf.24 <- 
  foreach(ntree = rep(10, ntasks), .combine = combine,
          .multicombine=TRUE, .packages='randomForest',
          .options.snow=opts) %dopar% {
            randomForest(overall_LS ~., data = dataset_used.rf, 
                         na.action = na.omit, ntree = 1000,
                         importance = T, mtry = 8)
          }
# do SNOW
