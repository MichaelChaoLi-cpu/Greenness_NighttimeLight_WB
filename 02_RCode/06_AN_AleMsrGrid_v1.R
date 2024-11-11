# Author: M.L.

# input: 04_dataset_used.RData
# 04_dataset_used.RData: "ID", the respondent id,
#                        "post_code", this is postal code of respondents.
#                        ...
#                        "overall_LS", output variable.
#                        "age", "high_stress", "low_stress", "easy_to_relax"
#                        "good_for_living", "live_environment_satefy",
#                        "community_attachment", "self_reported_health",
#                        "female", "student", "worker", "company_owner", 
#                        "government_officer", "self_employed", "professional",
#                        "housewife", "retired", "unemployed",
#                        "college_no_diploma", "bachelor", "master", "phd",
#                        "income_indiv", "NDVI", "NTL" (24 features)

# input: 07_MRS.result.NDVI.NTL.RData
# 07_MRS.result.NDVI.NTL.RData: Marginal substitue rate of NDVI and NTL

# input: 05_spatial.post.id.RData
# 05_spatial.post.id.RData: "post_code", this is postal code of respondents.
# Note: this is spatial point data frame of "post_code"

# output: 08_MRS.result.NDVI.NTL.with.loc.RData
# 08_MRS.result.NDVI.NTL.with.loc.RData: MSR with location.

# output: 09_coords.deleteNA.RData
# 09_coords.deleteNA.RData: "id", this is grid id.
#                           "MRS.NDVI": the gridded average value of monetary values
#                                       of NDVI
#                           "MRS.NTL": the gridded average value of monetary values
#                                      of NTL

# end

library(randomForest)
library(tidyverse)
library(sp)
library(rgdal)
library(spdplyr)

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

# make the raster -180 -60 180 60
nx = 86                                       # number of cells in the x direction
ny = 97                                     # number of cells in the y direction
xmin = 122.875                                     # x coordinate of lower, left cell center 
ymin = 23.875                                     # y coordinate of lower, left cell center 
xsize = 0.25                                   # extent of cells in x direction
ysize = 0.25                                   # extent of cells in y direction
proj <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0" 

addcoord <- function(nx,xmin,xsize,ny,ymin,ysize,proj) { # Michael Pyrcz, March, 2018                      
  # makes a 2D dataframe with coordinates based on GSLIB specification
  coords = matrix(nrow = nx*ny,ncol=2)
  ixy = 1
  for(iy in 1:nx) {
    for(ix in 1:ny) {
      coords[ixy,1] = xmin + (ix-1)*xsize  
      coords[ixy,2] = ymin + (iy-1)*ysize 
      ixy = ixy + 1
    }
  }
  coords.df = data.frame(coords)
  colnames(coords.df) <- c("X","Y")
  coords.df$id = 1:nrow(coords.df)
  xy <- coords.df[,c(1,2)]
  coords.df <- SpatialPointsDataFrame(coords = xy, data = coords.df %>% dplyr::select("id"),
                                      proj4string = CRS(proj))
  return (coords.df)
  
}

coords <- addcoord(nx,xmin,xsize,ny,ymin,ysize,proj)

coords <- as(coords, 'SpatialPixelsDataFrame')
coords <- as(coords, 'SpatialPolygonsDataFrame')

load("03_Results/08_MRS.result.NDVI.NTL.with.loc.RData")
xy <- dataset_used.rf.merge %>% dplyr::select(lon, lat)
MRS.result.sp <- SpatialPointsDataFrame(coords = xy, data = dataset_used.rf.merge[,c(1, 2, 3, 4, 5, 6, 7)],
                                                   proj4string = CRS(proj))
rm(xy)

grid.data <- over(coords, MRS.result.sp[,"MRS.NDVI"], fn = mean)
coords$MRS.NDVI <- grid.data$MRS.NDVI
grid.data <- over(coords, MRS.result.sp[,"MRS.NTL"], fn = mean)
coords$MRS.NTL <- grid.data$MRS.NTL
MRS.result.sp$count <- 1
grid.data <- over(coords, MRS.result.sp[,"count"], fn = sum)
coords$count <- grid.data$count

coords.deleteNA <- coords %>% filter(!is.na(MRS.NDVI))
coords.dropLowCount <- coords.deleteNA %>% filter(count > 30)

save(coords.deleteNA, coords.dropLowCount, file = "03_Results/09_coords.deleteNA.RData")
