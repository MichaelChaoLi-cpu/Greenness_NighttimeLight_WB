# Author: M.L.

# output: 01_data_pool.RData
# 01_data_pool.RData: raw data set from the survey. In this data set, the 
#                     features of interest are renamed.
# Note: this is a process file.

# output: 02_NTLRasterDataset.RData
# 02_NTLRasterDataset.RData: "post_code", this is postal code of respondents.
#                            "NTL", represents NTL values of a single day
#                            "year", the year of data
#                            "month", the month of data
# Note: this is a process file.

# output: 02_NTLRasterDataset_ag.RData
# 02_NTLRasterDataset_ag.RData: "post_code", this is postal code of respondents.
#                               "NTL", represents annual average NTL values
#                               "year", the year of data
# Note: this is a process file.

# output: 03_NDVIRasterDataset.RData
# 03_NDVIRasterDataset.RData: "post_code", this is postal code of respondents.
#                             "NDVI", represents NDVI values of a single day
#                             "year", the year of data
#                             "month", the month of data
# Note: this is a process file.

# output: 03_NDVIRasterDataset_ag.RData
# 03_NDVIRasterDataset_ag.RData: "post_code", this is postal code of respondents.
#                                "NDVI", represents annual average NTL values
#                                "year", the year of data
# Note: this is a process file.

# output: 04_dataset_used.RData
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

# output: 09_X_29IndVar.csv
# 09_X_29IndVar.csv: "year", "lat", "lon","female", 
#                    "age", "high_stress", "low_stress",
#                    "easy_to_relax", "good_for_living", "live_environment_satefy",
#                    "community_attachment", "income", "self_reported_health",
#                    "student", "worker", "company_owner", 
#                    "government_officer", "self_employed", 
#                    "professional", "housewife", "retired", "unemployed",
#                    "college_no_diploma", "bachelor", "master", "phd",
#                    "income_indiv", "NDVI", "NTL" (29 features)

# output: 10_y_29IndVar.csv
# 10_y_29IndVar.csv: "overall_LS"

# end

library(tidyverse)
library(readr)
library("dplyr")
library(haven)
library(readxl)
library(foreign)
library(sp)
library(rgdal)
library(raster)

extractBufferDataFromRaster <- function(RasterFolder, filelist, cityLocationSpatialPoint,
                                        year_start_location, month_start_location, flip_reverse = T,
                                        aimed_column_name = "raw", year_end_location = year_start_location + 3,
                                        month_end_location = month_start_location + 1
){
  RasterDataset <- 
    data.frame(Doubles=double(),
               Ints=integer(),
               Factors=factor(),
               Logicals=logical(),
               Characters=character(),
               stringsAsFactors=FALSE)
  for (filename in filelist){
    test_tiff <- raster::raster(paste0(RasterFolder, filename))
    if(flip_reverse){
      test_tiff <- flip(test_tiff, direction = 'y')
    }
    cat(filename)
    cat("\n")
    #crs(test_tiff) <- proj
    Year <- str_sub(filename, year_start_location, year_end_location) %>% as.numeric()
    Month <- str_sub(filename, month_start_location, month_end_location) %>% as.numeric()
    
    data_ext <- raster::extract(test_tiff, cityLocationSpatialPoint, fun = mean, na.rm = TRUE)
    cityLocationSpatialPoint@data$raw <- data_ext
    monthly_data <- cityLocationSpatialPoint@data %>%
      dplyr::select(post_code, raw)
    monthly_data <- monthly_data %>%
      mutate(year = Year,
             month = Month)
    RasterDataset <- rbind(RasterDataset, monthly_data)
  }
  colnames(RasterDataset) <- c("post_code", aimed_column_name, "year", "month")
  return(RasterDataset)
}

# the data in 2015
survey_2015 <- 
  read.csv(file = 'F:/15_Article/01_RawData/2015raw.csv', sep = ";", encoding = "UTF-8")

survey_2015 <- survey_2015 %>%
  drop_na(ssdb_id) %>%
  dplyr::select(ssdb_id, t18_q1, t18_q2, t18_q4, t18_q6, t18_q7, t18_q8, t18_q9,
                t18_q9s1, t18_q10s1, t18_q10s2, t18_q10s3, t18_q10s4,
                t18_q10s5, t18_q10s6, t18_q82, t18_q83,
                t18_q85, t18_q87_1, t18_q90) %>%
  rename(  ID = ssdb_id, gender = t18_q1 , age = t18_q2, post = t18_q4,
           high_stress = t18_q6, low_stress = t18_q7,
           easy_to_relax = t18_q8, overall_happiness = t18_q9 ,
           relative_happiness = t18_q9s1, overall_LS = t18_q10s1,
           relative_LS = t18_q10s2, LS_change = t18_q10s3, 
           good_for_living = t18_q10s4 , live_environment_satefy = t18_q10s5,
           community_attachment = t18_q10s6,  number_family =t18_q82,
           job = t18_q83, income = t18_q85 , education_background = t18_q87_1,
           self_reported_health = t18_q90 
  ) %>%
  mutate(year = 2015)

survey_2015$gender <- survey_2015$gender %>% as.numeric()
survey_2015$age <- survey_2015$age %>% as.numeric()
survey_2015$easy_to_relax <- survey_2015$easy_to_relax %>% as.numeric()
survey_2015$LS_change <- survey_2015$LS_change %>% as.numeric()


age_gender <- survey_2015 %>%
  dplyr::select(ID, gender, age, education_background)

# the data in 2016
survey_2016 <- 
  read.csv(file = 'F:/15_Article/01_RawData/2016raw.csv', encoding = "UTF-8")
survey_2016 <- survey_2016 %>%
  dplyr::select(ssdbid, t24_q11_1, t24_q11_2, t24_q12, t24_q3_1, t24_q3_2, t24_q4_1,
                t24_q4_2, t24_q5, t24_q7, t24_q8, t24_q9, t24_q44_1, t24_q46,
                t24_q47_1, t24_q48, t24_q2) %>%
  rename(ID = ssdbid, post = t24_q2,
         high_stress = t24_q11_1, low_stress = t24_q11_2,
         easy_to_relax = t24_q12, overall_happiness = t24_q3_1,
         relative_happiness = t24_q3_2, overall_LS = t24_q4_1,
         relative_LS = t24_q4_2, LS_change = t24_q5, 
         good_for_living = t24_q7, live_environment_satefy = t24_q8,
         community_attachment = t24_q9,  number_family = t24_q44_1,
         job = t24_q46, income = t24_q47_1,
         self_reported_health = t24_q48)

survey_2016 <- left_join(survey_2016, age_gender) %>%
  mutate(age2 = age + 1) %>%
  dplyr::select(-age) %>%
  rename(age = age2) %>%
  mutate(year = 2016)

# the data in 2017
survey_2017 <- 
  read.csv(file = 'F:/15_Article/01_RawData/2017raw.csv', encoding = "UTF-8")
survey_2017 <- survey_2017 %>%
  dplyr::select(ssdb_id, t27_q12_1, t27_q12_2, t27_q13, t27_q4_1, t27_q4_2,
                t27_q5_1, t27_q5_2, t27_q6, t27_q8, t27_q9, t27_q10, t27_q3_1,
                t27_q40_1, t27_q41_1, t27_q43_7, t27_q2) %>%
  rename(ID = ssdb_id, post = t27_q2,
         high_stress = t27_q12_1, low_stress = t27_q12_2,
         easy_to_relax = t27_q13, overall_happiness = t27_q4_1,
         relative_happiness = t27_q4_2, overall_LS = t27_q5_1,
         relative_LS = t27_q5_2, LS_change = t27_q6, 
         good_for_living = t27_q8, live_environment_satefy = t27_q9,
         community_attachment = t27_q10,  number_family = t27_q3_1,
         job = t27_q40_1, income = t27_q41_1,
         self_reported_health = t27_q43_7)

survey_2017 <- left_join(survey_2017, age_gender) %>%
  mutate(age2 = age + 2) %>%
  dplyr::select(-age) %>%
  rename(age = age2) %>%
  mutate(year = 2017)

# drop age_gender dataset
rm(age_gender)

spatial.post.id <- readOGR(dsn = 'F:/15_Article/01_RawData', layer = "point_with_post")
proj <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0" 
location.dataset <- spatial.post.id@data
location.dataset <- location.dataset %>% rename(post = post_code)
save(spatial.post.id, file = "01_Data/05_spatial.post.id.RData")

#append the dataset: 3 years to 1 years
data_pool <- rbind(survey_2015, survey_2016)
data_pool <- rbind(data_pool, survey_2017)

data_pool <- left_join(data_pool, location.dataset, by = "post")
data_pool <- data_pool %>% drop_na(gender) %>%
  mutate(female = gender - 1) %>%
  dplyr::select(-gender) %>%
  mutate(age_u_44 = ifelse(age < 45, 1, 0),
         age_45_64 = ifelse(age > 44 & age < 65, 1, 0),
         age_o_65 = ifelse(age > 64, 1, 0)) %>%
  mutate(student = ifelse(job < 4, 1, 0),
         worker = ifelse(job > 3 &  job < 8, 1, 0),
         company_owner = ifelse(job == 8, 1, 0),
         government_officer = ifelse(job == 9, 1, 0),
         self_employed = ifelse(job == 10, 1, 0),
         professional = ifelse(job == 11, 1, 0),
         housewife = ifelse(job == 12, 1, 0),
         retired = ifelse(job == 13, 1, 0),
         unemployed = ifelse(job == 14 | job == 15, 1, 0)
  ) %>%
  dplyr::select(-job, -number_family) %>%
  mutate(college_no_diploma = ifelse(education_background == 6 | education_background == 7, 1, 0),
         bachelor = ifelse(education_background == 8, 1, 0),
         master = ifelse(education_background == 9, 1, 0),
         phd = ifelse(education_background == 10, 1, 0)
  ) %>%
  dplyr::select(-education_background) %>%
  mutate(
    income_indiv = ifelse(income == 1, 1,
                          ifelse(income ==2, 2.5,
                                 ifelse(income == 3, 3.5,
                                        ifelse(income == 4, 4.5,
                                               ifelse(income == 5 ,5.5,
                                                      ifelse(income == 6, 6.5,
                                                             ifelse(income == 7, 7.5,
                                                                    ifelse(income ==8, 8.5,
                                                                           ifelse(income == 9, 9.5, 
                                                                                  ifelse(income == 10, 12.5,
                                                                                         ifelse(income == 11, 17.5,
                                                                                                ifelse(income == 12, 25,
                                                                                                       ifelse(income == 13, 30, NA)))))))))))))
  )
data_pool <- data_pool %>% rename(post_code = post)
save(data_pool, file = "01_Data/01_data_pool.RData")

# get NTL data mean value
spatial.post.id.buffer <- rgeos::gBuffer(spatial.post.id, byid = T, width = 0.05)
NTLRasterFolder <- "F:/15_Article/02_RasterData/NTL/"
filelist <- list.files(NTLRasterFolder)
filelist.tif <- c()
for (name in filelist){
  if(name %>% stringr::str_sub(-3, -1) == "tif"){
    filelist.tif <- append(filelist.tif, name)
  }
}
NTLRasterDataset <- 
  extractBufferDataFromRaster(NTLRasterFolder, filelist.tif, spatial.post.id.buffer,
                             11, 15, F, "NTL")
save(NTLRasterDataset, file = "01_Data/02_NTLRasterDataset.RData")
NTLRasterDataset_ag <- aggregate(NTLRasterDataset$NTL,
                                  by = list(NTLRasterDataset$post_code, 
                                            NTLRasterDataset$year
                                  ), 
                                  FUN = "mean", na.rm = T
)
colnames(NTLRasterDataset_ag) <- c("post_code", "year", "NTL")
save(NTLRasterDataset_ag, file = "01_Data/02_NTLRasterDataset_ag.RData")

NDVIRasterFolder <- "F:/15_Article/02_RasterData/NDVI/VI_16Days_500m_v6/NDVI/"
filelist <- list.files(NDVIRasterFolder)
filelist.tif <- c()
for (name in filelist){
  if(name %>% stringr::str_sub(-3, -1) == "tif"){
    filelist.tif <- append(filelist.tif, name)
  }
}
NDVIRasterDataset <- 
  extractBufferDataFromRaster(NDVIRasterFolder, filelist.tif, spatial.post.id.buffer,
                              14, 19, F, "NDVI", month_end_location = 21)
save(NDVIRasterDataset, file = "01_Data/03_NDVIRasterDataset.RData")
NDVIRasterDataset$date <- 
  as.Date((NDVIRasterDataset$month - 1),
          origin = paste0(NDVIRasterDataset$year,"-01-01")) %>% as.character()
NDVIRasterDataset$month <- str_sub(NDVIRasterDataset$date, 6, 7) %>% as.numeric()
NDVIRasterDataset_ag <- aggregate(NDVIRasterDataset$NDVI,
                               by = list(NDVIRasterDataset$post_code, 
                                         NDVIRasterDataset$year
                                         ), 
                               FUN = "mean", na.rm = T
)
colnames(NDVIRasterDataset_ag) <- c("post_code", "year", "NDVI")
NDVIRasterDataset_ag$NDVI <- NDVIRasterDataset_ag$NDVI / 10000 * 100  #convert into from 100% to -100% 
save(NDVIRasterDataset_ag, file = "01_Data/03_NDVIRasterDataset_ag.RData")

dataset_used <- left_join(data_pool, NDVIRasterDataset_ag, by = c("post_code", "year"))
dataset_used <- left_join(dataset_used, NTLRasterDataset_ag, by = c("post_code", "year"))
save(dataset_used, file = "01_Data/04_dataset_used.RData")

dataset_toXY <- dataset_used %>% dplyr::select("overall_LS","year", "lat", "lon","female", 
                                               "age", "high_stress", "low_stress",
                                               "easy_to_relax", "good_for_living", "live_environment_satefy",
                                               "community_attachment", "income", "self_reported_health",
                                               "student", "worker", "company_owner", 
                                               "government_officer", "self_employed", 
                                               "professional", "housewife", "retired", "unemployed",
                                               "college_no_diploma", "bachelor", "master", "phd",
                                               "income_indiv", "NDVI", "NTL"
                                                ) %>% na.omit()
dataset_toXY %>% dplyr::select(-"overall_LS") %>% write.csv(file = "01_Data/09_X_LSoverall_29IndVar.csv")
dataset_toXY %>% dplyr::select("overall_LS") %>% write.csv(file = "01_Data/10_y_LSoverall_29IndVar.csv")

dataset_toXY <- dataset_used %>% dplyr::select("overall_happiness","year", "lat", "lon","female", 
                                               "age", "high_stress", "low_stress",
                                               "easy_to_relax", "good_for_living", "live_environment_satefy",
                                               "community_attachment", "income", "self_reported_health",
                                               "student", "worker", "company_owner", 
                                               "government_officer", "self_employed", 
                                               "professional", "housewife", "retired", "unemployed",
                                               "college_no_diploma", "bachelor", "master", "phd",
                                               "income_indiv", "NDVI", "NTL"
) %>% na.omit()
dataset_toXY %>% dplyr::select(-"overall_happiness") %>% write.csv(file = "01_Data/11_X_Happinessoverall_29IndVar.csv")
dataset_toXY %>% dplyr::select("overall_happiness") %>% write.csv(file = "01_Data/12_y_Happinessoverall.csv")

dataset_toXY <- dataset_used %>% dplyr::select("relative_LS","year", "lat", "lon","female", 
                                               "age", "high_stress", "low_stress",
                                               "easy_to_relax", "good_for_living", "live_environment_satefy",
                                               "community_attachment", "income", "self_reported_health",
                                               "student", "worker", "company_owner", 
                                               "government_officer", "self_employed", 
                                               "professional", "housewife", "retired", "unemployed",
                                               "college_no_diploma", "bachelor", "master", "phd",
                                               "income_indiv", "NDVI", "NTL"
) %>% na.omit()
dataset_toXY %>% dplyr::select(-"relative_LS") %>% write.csv(file = "01_Data/13_X_LSrelative_29IndVar.csv")
dataset_toXY %>% dplyr::select("relative_LS") %>% write.csv(file = "01_Data/14_y_LSrelative_29IndVar.csv")

dataset_toXY <- dataset_used %>% dplyr::select("relative_happiness","year", "lat", "lon","female", 
                                               "age", "high_stress", "low_stress",
                                               "easy_to_relax", "good_for_living", "live_environment_satefy",
                                               "community_attachment", "income", "self_reported_health",
                                               "student", "worker", "company_owner", 
                                               "government_officer", "self_employed", 
                                               "professional", "housewife", "retired", "unemployed",
                                               "college_no_diploma", "bachelor", "master", "phd",
                                               "income_indiv", "NDVI", "NTL"
) %>% na.omit()
dataset_toXY %>% dplyr::select(-"relative_happiness") %>% write.csv(file = "01_Data/15_X_Happinessrelative_29IndVar.csv")
dataset_toXY %>% dplyr::select("relative_happiness") %>% write.csv(file = "01_Data/16_y_Happinessrelative.csv")
