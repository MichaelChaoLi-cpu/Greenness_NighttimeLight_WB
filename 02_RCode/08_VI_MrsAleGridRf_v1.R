# Author: M.L.

# Visualization

# end

library(sp)
library(tmap)

title_size = .0002
legend_title_size = 2
margin = 0
tmap_mode('plot')
bound <- raster::getData("GADM", country="JPN", level=1)
proj <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"
bound@bbox[1,2] <- 147 
bound@data$pref_num <- str_sub(bound@data$GID_1,5,-3)
bound@data$pref_num <- bound@data$pref_num %>% as.numeric()
bound@data$pref_num1 <- NA
bound@data <- bound@data %>%
  mutate(
    pref_num1 = ifelse(pref_num == 12, 1, pref_num1),
    pref_num1 = ifelse(pref_num == 3, 2, pref_num1),
    pref_num1 = ifelse(pref_num == 16, 3, pref_num1),
    pref_num1 = ifelse(pref_num == 24, 4, pref_num1),
    pref_num1 = ifelse(pref_num == 2, 5, pref_num1),
    pref_num1 = ifelse(pref_num == 45, 6, pref_num1),
    pref_num1 = ifelse(pref_num == 8, 7, pref_num1),
    pref_num1 = ifelse(pref_num == 14, 8, pref_num1),
    pref_num1 = ifelse(pref_num == 39, 9, pref_num1),
    pref_num1 = ifelse(pref_num == 10, 10, pref_num1),
    pref_num1 = ifelse(pref_num == 35, 11, pref_num1),
    pref_num1 = ifelse(pref_num == 4, 12, pref_num1),
    pref_num1 = ifelse(pref_num == 41, 13, pref_num1),
    pref_num1 = ifelse(pref_num == 19, 14, pref_num1),
    pref_num1 = ifelse(pref_num == 29, 15, pref_num1),
    pref_num1 = ifelse(pref_num == 43, 16, pref_num1),
    pref_num1 = ifelse(pref_num == 15, 17, pref_num1),
    pref_num1 = ifelse(pref_num == 6, 18, pref_num1),
    pref_num1 = ifelse(pref_num == 47, 19, pref_num1),
    pref_num1 = ifelse(pref_num == 26, 20, pref_num1),
    pref_num1 = ifelse(pref_num == 9, 21, pref_num1),
    pref_num1 = ifelse(pref_num == 38, 22, pref_num1),
    pref_num1 = ifelse(pref_num == 1, 23, pref_num1),
    pref_num1 = ifelse(pref_num == 23, 24, pref_num1),
    pref_num1 = ifelse(pref_num == 36, 25, pref_num1),
    pref_num1 = ifelse(pref_num == 22, 26, pref_num1),
    pref_num1 = ifelse(pref_num == 33, 27, pref_num1),
    pref_num1 = ifelse(pref_num == 13, 28, pref_num1),
    pref_num1 = ifelse(pref_num == 28, 29, pref_num1),
    pref_num1 = ifelse(pref_num == 44, 30, pref_num1),
    pref_num1 = ifelse(pref_num == 42, 31, pref_num1),
    pref_num1 = ifelse(pref_num == 37, 32, pref_num1),
    pref_num1 = ifelse(pref_num == 31, 33, pref_num1),
    pref_num1 = ifelse(pref_num == 11, 34, pref_num1),
    pref_num1 = ifelse(pref_num == 46 , 35, pref_num1),
    pref_num1 = ifelse(pref_num == 40 , 36, pref_num1),
    pref_num1 = ifelse(pref_num == 17 , 37, pref_num1),
    pref_num1 = ifelse(pref_num == 5 , 38, pref_num1),
    pref_num1 = ifelse(pref_num == 20 , 39, pref_num1),
    pref_num1 = ifelse(pref_num == 7 , 40, pref_num1),
    pref_num1 = ifelse(pref_num == 34 , 41, pref_num1),
    pref_num1 = ifelse(pref_num == 27 , 42, pref_num1),
    pref_num1 = ifelse(pref_num == 21 , 43, pref_num1),
    pref_num1 = ifelse(pref_num == 30 , 44, pref_num1),
    pref_num1 = ifelse(pref_num == 25 , 45, pref_num1),
    pref_num1 = ifelse(pref_num == 18 , 46, pref_num1),
    pref_num1 = ifelse(pref_num == 32 , 47, pref_num1)
  )
pref_note_1 <- 
  paste("1 Hokkaido\n2 Aomori\n3 Iwate\n4 Miyagi\n5 Akita\n6 Yamagata\n7 Fukushima\n",
        "8 Ibaraki\n9 Tochigi\n10 Gunma\n",
        sep = "")
pref_note_2 <- 
  paste("11 Saitama\n12 Chiba\n13 Tokyo\n14 Kanagawa\n",
        "15 Niigata\n16 Toyama\n17 Ishikawa\n18 Fukui\n19 Yamanashi\n20 Nagano\n",
        sep = "")
pref_note_3 <- 
  paste("21 Gifu\n22 Shizuoka\n23 Aichi\n24 Mie\n",
        "25 Shiga\n26 Kyoto\n27 Osaka\n28 Hyogo\n29 Nara\n30 Wakayama\n",
        sep = "")
pref_note_4 <- 
  paste("31 Tottori\n32 Shimane\n33 Okayama\n34 Hiroshima\n35 Yamaguchi\n",
        "36 Tokushima\n37 Kagawa\n38 Ehime\n39 Kochi\n40 Fukuoka\n",
        sep = "")
pref_note_5 <- 
  paste("41 Saga\n",
        "42 Nagasaki\n43 Kumamoto\n44 Oita\n45 Miyazaki\n46 Kagoshima\n",
        "47 Okinawa\n\n\n\n",
        sep = "")
proj4string(bound) <- CRS(proj)

load("03_Results/09_meshFile.deleteNA.RData")
pal <- colorRampPalette(c("blue","green", "white", "yellow","red"))
brks = seq(-1, 1, 0.2)
labels_brks <- c("< -1", "", "-0.6", "", "-0.2", "0",
                 "0.2", "", "0.6", "", "1")
(MRS.NDVI <-
  tm_shape(bound, bbox = bound@bbox) +
  tm_polygons(col = 'GID_0', lwd = 0.01, alpha = .6, pal = "grey85", legend.show = F) +
  tm_shape(coords.dropLowCount) +
  tm_polygons(col = 'MRS.NDVI', pal = pal(11), auto.palette.mapping = FALSE,
          border.alpha = 0,  breaks = brks, style = 'cont', 
          legend.is.portrait = F, title = "The Monetary Value of NDVI (million JPY/1%)",
          labels = labels_brks, midpoint = 0) +
  tm_shape(bound) +
  tm_polygons(col = 'GID_0', lwd = 0.01, alpha = .0, pal = NULL, legend.show = F) +
  tm_text("pref_num1", remove.overlap = F, size = legend_title_size * 0.35, auto.placement = F, alpha = 1) +
  tm_grid(projection = proj, alpha = .25) + 
  tm_layout(
    inner.margins = c(margin, margin, margin, margin),
    title.size = title_size, 
    legend.position = c("left", "top"),
    legend.title.size = legend_title_size,
    legend.text.size = legend_title_size * 0.75,
  ) +
  tm_credits("Prefecture:", size = 1, position = c(0.48, 0.28)) +
  tm_credits(pref_note_1, position = c(0.48, 0.05)) +
  tm_credits(pref_note_2, position = c(0.58, 0.05)) +
  tm_credits(pref_note_3, position = c(0.68, 0.05)) +
  tm_credits(pref_note_4, position = c(0.78, 0.05)) +
  tm_credits(pref_note_5, position = c(0.88, 0.05)) +
  tm_compass(type = "arrow", position = c("right", "bottom")) +
  tm_scale_bar() )
MRS.NDVI %>%
  tmap_save(filename = "04_Figure//06_MRS.NDVI.jpg" ,width = 210, height = 220, units = 'mm', dpi = 1000)



coords.deleteNA$MRS.NTL %>% hist()
brks = seq(-1, 1, 0.2)
labels_brks <- c("< -1", "", "-0.6", "", "-0.2", "0",
                 "0.2", "", "0.6", "", "1")

labels_brks <- c("< -0.1", "", "-0.06", "", "-0.02", "0",
                 "0.2", "", "0.6", "", "1")
coords.dropLowCount$MRS.NTL.dou.neg <- coords.dropLowCount$MRS.NTL
coords.dropLowCount@data <- coords.dropLowCount@data %>%
  mutate(MRS.NTL.dou.neg = ifelse(MRS.NTL.dou.neg<0, MRS.NTL.dou.neg*10, MRS.NTL.dou.neg))

(MRS.NTL <-
  tm_shape(bound, bbox = bound@bbox) +
  tm_polygons(col = 'GID_0', lwd = 0.01, alpha = .6, pal = "grey85", legend.show = F) +
  tm_shape(coords.dropLowCount) +
  tm_polygons(col = 'MRS.NTL.dou.neg', pal = pal(11), auto.palette.mapping = FALSE,
              border.alpha = 0,  breaks = brks, style = 'cont', 
              legend.is.portrait = F, title = "The Monetary Value of NTL (million JPY/1 Unit)",
              labels = labels_brks, midpoint = 0) +
  tm_shape(bound) +
  tm_polygons(col = 'GID_0', lwd = 0.01, alpha = .0, pal = NULL, legend.show = F) +
  tm_text("pref_num1", remove.overlap = F, size = legend_title_size * 0.35, auto.placement = F, alpha = 1) +
  tm_grid(projection = proj, alpha = .25) + 
    tm_layout(
      inner.margins = c(margin, margin, margin, margin),
      title.size = title_size, 
      legend.position = c("left", "top"),
      legend.title.size = legend_title_size,
      legend.text.size = legend_title_size * 0.75,
    ) +
    tm_credits("Prefecture:", size = 1, position = c(0.48, 0.28)) +
    tm_credits(pref_note_1, position = c(0.48, 0.05)) +
    tm_credits(pref_note_2, position = c(0.58, 0.05)) +
    tm_credits(pref_note_3, position = c(0.68, 0.05)) +
    tm_credits(pref_note_4, position = c(0.78, 0.05)) +
    tm_credits(pref_note_5, position = c(0.88, 0.05)) +
    tm_compass(type = "arrow", position = c("right", "bottom")) +
    tm_scale_bar() )
MRS.NTL %>%
  tmap_save(filename = "04_Figure//07_MRS.NTL.jpg" ,width = 210, height = 220, units = 'mm', dpi = 1000)
