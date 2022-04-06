# Author: M.L.



# end

library(tidyverse)
library("dplyr")
library(plm)

load("01_Data/04_dataset_used.RData")

dataset_used <- dataset_used %>%
  mutate(live_environment_satefy = ifelse(live_environment_satefy==0, NA, live_environment_satefy))
dataset_used <- dataset_used %>%
  mutate(NTL_log = ifelse(NTL < 0, 0, NTL))
dataset_used$NTL_log <- log(dataset_used$NTL_log + 1)
dataset_used$NTL_log %>% hist()

pdata <- pdata.frame(dataset_used, index = c("ID", "year"))

formula <- live_environment_satefy ~ female + age + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd + good_for_living + community_attachment + NTL_log

cor(dataset_used %>% dplyr::select(all.vars(formula)) %>% na.omit())

ols <- plm(formula = formula, pdata, effect = "individual", model = "pooling")
summary(ols)

#rem <- plm(formula = formula, pdata, effect = "individual", model = "random")
#summary

formula_high_stress <- high_stress ~ female + age + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd + good_for_living + community_attachment + NTL_log
ols_high_stress <- plm(formula = formula_high_stress, pdata, effect = "individual", model = "pooling")
summary(ols_high_stress)

formula_low_stress <- low_stress ~ female + age + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd + good_for_living + community_attachment + NTL_log
ols_low_stress <- plm(formula = formula_low_stress, pdata, effect = "individual", model = "pooling")
summary(ols_low_stress)

formula_ha <- overall_happiness ~ live_environment_satefy + female + age + 
  self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd + good_for_living + community_attachment + NDVI 

ols_ha <- plm(formula = formula_ha, pdata, effect = "individual", model = "pooling")
summary(ols_ha)

#rem <- plm(formula = formula, pdata, effect = "individual", model = "random")
#summary(rem)

