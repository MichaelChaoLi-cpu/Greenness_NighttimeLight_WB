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
dataset_used$age2 <- dataset_used$age * dataset_used$age

pdata <- pdata.frame(dataset_used, index = c("ID", "year"))

### safety
formula_safe <- live_environment_satefy ~ female + age + age2 + self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd  + NTL_log + NDVI

cor(dataset_used %>% dplyr::select(all.vars(formula)) %>% na.omit())

ols_safe <- plm(formula = formula_safe, pdata, effect = "individual", model = "pooling")
summary(ols_safe)

rem_safe <- plm(formula = formula_safe, pdata, effect = "individual", model = "random")
summary(rem_safe)

### good for living
formula_goodLiving <- good_for_living ~ female + age +age2 + self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd  + NTL_log + NDVI

ols_goodLiving <- plm(formula = formula_goodLiving, pdata, effect = "individual", model = "pooling")
summary(ols_goodLiving)

rem_goodLiving <- plm(formula = formula_goodLiving, pdata, effect = "individual", model = "random")
summary(rem_goodLiving)

### community attachment
formula_attach <- community_attachment ~ female + age + age2 + self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd  + NTL_log +NDVI

ols_attach <- plm(formula = formula_attach, pdata, effect = "individual", model = "pooling")
summary(ols_attach)

rem_attach <- plm(formula = formula_attach, pdata, effect = "individual", model = "random")
summary(rem_attach)

### high stress
formula_high_stress <- high_stress ~ female + age + age2 + self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd + NTL_log + NDVI

ols_high_stress <- plm(formula = formula_high_stress, pdata, effect = "individual", model = "pooling")
summary(ols_high_stress)

rem_high_stress <- plm(formula = formula_high_stress, pdata, effect = "individual", model = "random")
summary(rem_high_stress)

### low stress
formula_low_stress <- low_stress ~ female + age + age2 + self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd +  NTL_log + NDVI
ols_low_stress <- plm(formula = formula_low_stress, pdata, effect = "individual", model = "pooling")
summary(ols_low_stress)

rem_low_stress <- plm(formula = formula_low_stress, pdata, effect = "individual", model = "random")
summary(rem_low_stress)



formula_ha <- overall_happiness ~ live_environment_satefy + 
  good_for_living + community_attachment + high_stress + low_stress +
  female + age + age2 + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd +  NDVI + NTL

ols_ha <- plm(formula = formula_ha, pdata, effect = "individual", model = "pooling")
summary(ols_ha)

rem_ha <- plm(formula = formula_ha, pdata, effect = "individual", model = "random")
summary(rem_ha)

