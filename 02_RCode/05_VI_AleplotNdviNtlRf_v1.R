# Author: M.L.

# end

library(randomForest)
library(tidyverse)
library(ALEPlot)
library(plotly)
library(ggplot2)

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

#####
(NDVI.line.pdp <- 
  ggplot(pdp.rf24.NDVI, aes(x = V2, y = result)) +
  geom_point(alpha = 0.5, shape = 16, color = "grey70", size  = 0.5))
  