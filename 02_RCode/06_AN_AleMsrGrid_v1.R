# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(sp)
library(rgdal)

run <- F
if(run){
  load("01_Data/04_dataset_used.RData")
  dataset_used <- dataset_used %>%
    mutate(live_environment_satefy = ifelse(live_environment_satefy==0, NA, live_environment_satefy))
  dataset_used <- dataset_used %>%
    mutate(NTL_log = ifelse(NTL < 0, 0, NTL))
  dataset_used$NTL_log <- log(dataset_used$NTL_log + 1)
  
  formula_LS <- overall_LS ~ live_environment_satefy + 
    good_for_living + community_attachment + high_stress + low_stress +
    female + age + self_reported_health + income_indiv + college_no_diploma +
    bachelor + master + phd +  NDVI + NTL_log
  
  dataset_used.rf.merge <- dataset_used %>% 
    dplyr::select(ID, post_code, all.vars(formula_LS), student:unemployed) %>% na.omit()
  
  load("03_Results/07_MRS.result.NDVI.NTL.RData")
  
  dataset_used.rf.merge <- left_join(dataset_used.rf.merge, ME.estimation.dataset.used)
  dataset_used.rf.merge <- dataset_used.rf.merge %>%
    dplyr::select(ID, post_code, ME.NDVI, ME.NTL, ME.income, MRS.NDVI, MRS.NTL)
  
  load("01_Data/05_spatial.post.id.RData")
  location.dataset <- spatial.post.id@data
  dataset_used.rf.merge <- left_join(dataset_used.rf.merge, location.dataset)
  save(dataset_used.rf.merge, file = "03_Results/08_MRS.result.NDVI.NTL.with.loc.RData")
}

meshFile <- readOGR(dsn = "C:/11_Article/01_Data/01_mesh", layer = "MeshFile")
meshFile@data <- meshFile@data %>% dplyr::select(G04d_001) 
meshFile@data$G04d_001 <- meshFile@data$G04d_001 %>% as.numeric()

load("03_Results/08_MRS.result.NDVI.NTL.with.loc.RData")
proj <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0" 
xy <- dataset_used.rf.merge %>% dplyr::select(lon, lat)
MRS.result.sp <- SpatialPointsDataFrame(coords = xy, data = dataset_used.rf.merge[,c(1, 2, 3, 4, 5, 6, 7)],
                                                   proj4string = CRS(proj))
rm(xy)

grid.data <- over(meshFile, MRS.result.sp[,"MRS.NDVI"], fn = mean)
meshFile$MRS.NDVI <- grid.data$MRS.NDVI
grid.data <- over(meshFile, MRS.result.sp[,"MRS.NTL"], fn = mean)
