# Author: M.L.



# end

library(tidyverse)
library("dplyr")
library(plm)
library(MASS)
library(erer)

load("01_Data/04_dataset_used.RData")

dataset_used <- dataset_used %>%
  mutate(live_environment_satefy = ifelse(live_environment_satefy==0, NA, live_environment_satefy))
dataset_used <- dataset_used %>%
  mutate(NTL_log = ifelse(NTL < 0, 0, NTL))
dataset_used$NTL_log <- log(dataset_used$NTL_log + 1)
dataset_used$NTL_log %>% hist()
dataset_used$age2 <- dataset_used$age * dataset_used$age

pdata <- pdata.frame(dataset_used, index = c("ID", "year"))


#### This is based on OLS
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

#### OLS

#### logit 
dataset_used$female <- dataset_used$female %>% as.factor()
dataset_used$self_reported_health <- dataset_used$self_reported_health %>% as.factor()
dataset_used$college_no_diploma <- dataset_used$college_no_diploma %>% as.factor()
dataset_used$bachelor <- dataset_used$bachelor %>% as.factor()
dataset_used$master <- dataset_used$master %>% as.factor()
dataset_used$phd <- 

dataset_used$live_environment_satefy_factor <- dataset_used$live_environment_satefy %>% as.factor()

formula_safe <- live_environment_satefy_factor ~ female + age +  self_reported_health +
  income_indiv + college_no_diploma + bachelor + master + phd  + NTL_log + NDVI
glm_safe <- polr(formula = formula_safe, data = dataset_used, Hess = T)
summary(glm_safe)

ocME(glm_safe)

dataset_used$overall_happiness <- dataset_used$overall_happiness %>% as.factor()
formula_ha <- overall_happiness ~ live_environment_satefy + 
  good_for_living + community_attachment + high_stress + low_stress +
  female + age + self_reported_health + income_indiv + college_no_diploma +
  bachelor + master + phd +  NDVI + NTL
glm_ha <- polr(formula = formula_ha, data = dataset_used, Hess = T)
summary(glm_ha)

ocME(glm_ha, digits = 5)
