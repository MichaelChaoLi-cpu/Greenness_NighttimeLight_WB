# Author: M.L.

# Visualization

# end

library(randomForest)
library(tidyverse)
library(ALEPlot)
library(plotly)
library(ggplot2)
library(grid)
library(gridExtra)
library(stargazer)

findBestFitFunction <- function(input_pdp, highest_order = 20, decide_value = 0.99, weights = NULL){
  if (!is.null(weights)){
    if(!(nrow(input_pdp)==length(weights))){stop("Weights have a different length with input data!")}
  }
  input_pdp <- input_pdp %>% as.matrix() %>% as.data.frame()
  input_pdp <- input_pdp %>% dplyr::select('yhat', dplyr::everything())
  y <- input_pdp %>% dplyr::select('yhat')
  x <- input_pdp %>% dplyr::select(-'yhat')
  for (order in seq(1,highest_order)){
    x[,paste0("order_", as.character(order))] <- input_pdp[,2]^order
  }
  x <- x[2:ncol(x)]
  r2_array <- c()
  first_time <- T
  if(is.null(weights)){cat('Unweighted!\n')} else{
    cat('Weighted!\n')
  }
  for (order in seq(1,highest_order)){
    data <- cbind(y, x[1:order])
    
    if(is.null(weights)) {
      regression <- lm(yhat ~ ., data)
      r2 <- summary(regression)$adj.r.squared
    } else {
      regression <- lm(yhat ~ ., data, weights = weights)
      r2 <- summary(regression)$adj.r.squared
    }
    if((r2>decide_value)&(first_time == T)){
      first_over_decide_value <- order
      keep.model <- regression
      first_time <- F
    }
    r2_array <- append(r2_array, r2)
  }
  if(first_time == T){
    first_over_decide_value <- NULL
    keep.model <- regression
  }
  cat(first_over_decide_value)
  result <- list(first_over_decide_value, r2_array, keep.model)
  return(result)
}

predictPDP <- function(input_pdp, decided_order = 20, weights_vector = NULL){
  if (is.null(decided_order)) {decided_order = 20}
  cat("decide order: ", decided_order)
  input_pdp <- input_pdp %>% as.matrix() %>% as.data.frame()
  input_pdp <- input_pdp %>% dplyr::select('yhat', dplyr::everything())
  y <- input_pdp %>% dplyr::select('yhat')
  x <- input_pdp %>% dplyr::select(-'yhat')
  for (order in seq(1,decided_order)){
    x[,paste0("order_", as.character(order))] <- input_pdp[,2]^order
  }
  x <- x[2:ncol(x)]
  data <- cbind(y, x)
  regression <- lm(yhat ~., data = data, weights = weights_vector)
  input_pdp$yhat_pred <- predict(regression, data)
  output_list <- list(input_pdp, regression)
  return(output_list)
}

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
  scale_x_continuous(name = "NDVI (%)") +
  scale_y_continuous(name = "LS Prediction - Accumulated Local Effects") +
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

NTL.line <- 
  ggplot(ale.dataframe, aes(x = NTL, y = LS, group = NDVI)) +
  geom_line(alpha = 0.05, size = 0.5) +
  scale_x_continuous(name = "Logarithm of NTL") +
  scale_y_continuous(name = "LS Prediction - Accumulated Local Effects") +
  theme_bw()
jpeg(file="04_Figure/04_NTL.line.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NTL.line
dev.off()

NTL.point <- 
  ggplot(ale.dataframe, aes(x = NTL, y = LS)) +
  geom_point(alpha = 0.5, shape = 16, color = "grey70", size  = 0.5) +
  geom_smooth() +
  theme_bw()
jpeg(file="04_Figure/05_NTL.point.jpeg", width = 297, height = 105, units = "mm", quality = 300, res = 300)
NTL.point
dev.off()
  
#####
load("03_Results/03_data.rf.24.PDP.NDVI.RData")
(NDVI.line.pdp <- 
  ggplot(pdp.rf24.NDVI) +
  geom_line( aes(x = V2, y = result), alpha = 0.5, color = "green3", size  = 1) +
  scale_x_continuous(name = "NDVI (%)") +
  scale_y_continuous(name = "LS Prediction - Partial Dependency Profile") +
  theme_bw() +
  annotate("text", x = 6, y = 3.39, label = 'bold("a")', parse = TRUE, size = 5))

  
load("03_Results/04_data.rf.24.PDP.NTL.RData")
(NTL.line.pdp <- 
    ggplot(pdp.rf24.NTL_log, aes(x = V2, y = result)) +
    geom_line(alpha = 0.5, color = "chocolate1", size  = 1) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Partial Dependency Profile") +
    theme_bw() +
    annotate("text", x = 0, y = 3.42, label = 'bold("b")', parse = TRUE, size = 5))

load("03_Results/05_data.rf.24.PDP.income.RData")
(income.line.pdp <- 
    ggplot(pdp.income.df, aes(x = V2, y = result)) +
    geom_line(alpha = 0.5, color = "magenta3", size  = 1) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Partial Dependency Profile") +
    theme_bw() +
    annotate("text", x = 0, y = 3.7, label = 'bold("c")', parse = TRUE, size = 5))

jpeg(file = "04_Figure/08_PDP.jpeg", width = 297, height = 90, units = "mm", quality = 300, res = 300)
grid.arrange(NDVI.line.pdp, NTL.line.pdp, income.line.pdp,
             nrow = 1)
dev.off()

load("03_Results/06_ALE.2.rf24.NDVI.NTL.only.500.RData")
(NDVI.line.ale <- 
    ggplot() +
    geom_line( aes(x = ALE.2.rf24.NDVI.only$x.values, y = ALE.2.rf24.NDVI.only$f.values),
               alpha = 0.5, color = "green3", size  = 1) +
    scale_x_continuous(name = "NDVI (%)") +
    scale_y_continuous(name = "LS Prediction - Accumulated Local Effects") +
    theme_bw() +
    annotate("text", x = 6, y = 0.06, label = 'bold("a")', parse = TRUE, size = 5))

(NTL.line.ale <- 
    ggplot() +
    geom_line(aes(x = ALE.2.rf24.NTL.only$x.values, y = ALE.2.rf24.NTL.only$f.values),
              alpha = 0.5, color = "chocolate1", size  = 1) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Partial Dependency Profile") +
    theme_bw() +
    annotate("text", x = 0, y = 0.09, label = 'bold("b")', parse = TRUE, size = 5))

(income.line.ale <- 
    ggplot() +
    geom_line(aes(x = ALE.2.rf24.income.only$x.values, y = ALE.2.rf24.income.only$f.values),
              alpha = 0.5, color = "magenta3", size  = 1) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Partial Dependency Profile") +
    theme_bw() +
    annotate("text", x = 0, y = 0.4, label = 'bold("c")', parse = TRUE, size = 5))

jpeg(file = "04_Figure/09_ALE.jpeg", width = 297, height = 90, units = "mm", quality = 300, res = 300)
grid.arrange(NDVI.line.ale, NTL.line.ale, income.line.ale,
             nrow = 1)
dev.off()

load("03_Results/10_Pseudo.funciton.ALE.RData")
(Fuction.NDVI.line.ale <- 
    ggplot(pred.ALE.NDVI.only[[1]], aes(x = NDVI)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "green3",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "NDVI (%)") +
    scale_y_continuous(name = "LS Prediction - Accumulated Local Effects") +
    theme_bw() +
    annotate("text", x = 6, y = 0.06, label = 'bold("a")', parse = TRUE, size = 5) +
    annotate("text", x = 21, y = -0.075, label = 'bold("R2 = 98.15%")', parse = TRUE, size = 5))

(Fuction.NTL.line.ale <- 
    ggplot(pred.ALE.NTL.only[[1]], aes(x = NTL)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "chocolate1",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Accumulated Local Effects") +
    theme_bw() +
    annotate("text", x = 0, y = 0.09, label = 'bold("b")', parse = TRUE, size = 5) +
    annotate("text", x = 0.8, y = -0.25, label = 'bold("R2 = 99.27%")', parse = TRUE, size = 5))

(Fuction.income.line.ale <- 
    ggplot(pred.ALE.income.only[[1]], aes(x = income)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "magenta3",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - Accumulated Local Effects") +
    theme_bw() +
    annotate("text", x = 0, y = 0.4, label = 'bold("c")', parse = TRUE, size = 5) +
    annotate("text", x = 25, y = -0.12, label = 'bold("R2 = 99.53%")', parse = TRUE, size = 5))

jpeg(file = "04_Figure/10_pseudoFun_ALE.jpeg", width = 297, height = 90,
     units = "mm", quality = 300, res = 300)
grid.arrange(Fuction.NDVI.line.ale, Fuction.NTL.line.ale, Fuction.income.line.ale,
             nrow = 1)
dev.off()

#-------------descriptive statistics--------------
Mean <- round(mean(dataset_used.rf$overall_LS), 2)
SD <- round(sd(dataset_used.rf$overall_LS), 2)
N = nrow(dataset_used.rf)
grob <- grobTree(textGrob(paste0("Mean = ", Mean, "\nStd.dev = ", SD,"\nN = ", N),
                          x = 0.75,  y = 0.90, hjust = 0,
                          gp = gpar(col = "black", fontsize = 10)))
grob_add <- grobTree(textGrob("a",
                              x = 0.02,  y = 0.95, hjust = 0,
                              gp = gpar(col = "black", fontsize = 20)))
(a <- ggplot(dataset_used.rf) +
    aes(x = overall_LS) +
    xlim(0, 6) +
    geom_histogram(colour = "black", fill = "white", bins = 5, binwidth = 1) +
    xlab("LS Assessment") + 
    ylab("Frequency") +
    annotation_custom(grob) +
    annotation_custom(grob_add) +
    theme_bw())

Mean <- round(mean(dataset_used.rf$NDVI), 2)
SD <- round(sd(dataset_used.rf$NDVI), 2)
N = nrow(dataset_used.rf)
grob <- grobTree(textGrob(paste0("Mean = ", Mean, "\nStd.dev = ", SD,"\nN = ", N),
                          x = 0.75,  y = 0.90, hjust = 0,
                          gp = gpar(col = "black", fontsize = 10)))
grob_add <- grobTree(textGrob("b",
                              x = 0.02,  y = 0.95, hjust = 0,
                              gp = gpar(col = "black", fontsize = 20)))
(b <- ggplot(dataset_used.rf) +
    aes(x = NDVI) +
    #xlim(0, 6) +
    geom_histogram(colour = "black", fill = "white", bins = 40, binwidth = 1) +
    xlab("NDVI (%)") + 
    ylab("Frequency") +
    annotation_custom(grob) +
    annotation_custom(grob_add) +
    theme_bw())

Mean <- round(mean(dataset_used.rf$NTL_log), 2)
SD <- round(sd(dataset_used.rf$NTL_log), 2)
N = nrow(dataset_used.rf)
grob <- grobTree(textGrob(paste0("Mean = ", Mean, "\nStd.dev = ", SD,"\nN = ", N),
                          x = 0.75,  y = 0.90, hjust = 0,
                          gp = gpar(col = "black", fontsize = 10)))
grob_add <- grobTree(textGrob("c",
                              x = 0.02,  y = 0.95, hjust = 0,
                              gp = gpar(col = "black", fontsize = 20)))
(c <- ggplot(dataset_used.rf) +
    aes(x = NTL_log) +
    #xlim(0, 6) +
    geom_histogram(colour = "black", fill = "white", bins = 40, binwidth = 0.1) +
    xlab("Logarithm of NTL") + 
    ylab("Frequency") +
    annotation_custom(grob) +
    annotation_custom(grob_add) +
    theme_bw())

Mean <- round(mean(dataset_used.rf$income_indiv), 2)
SD <- round(sd(dataset_used.rf$income_indiv), 2)
N = nrow(dataset_used.rf)
grob <- grobTree(textGrob(paste0("Mean = ", Mean, "\nStd.dev = ", SD,"\nN = ", N),
                          x = 0.75,  y = 0.90, hjust = 0,
                          gp = gpar(col = "black", fontsize = 10)))
grob_add <- grobTree(textGrob("d",
                              x = 0.02,  y = 0.95, hjust = 0,
                              gp = gpar(col = "black", fontsize = 20)))
(d <- ggplot(dataset_used.rf) +
    aes(x = income_indiv) +
    #xlim(0, 6) +
    geom_histogram(colour = "black", fill = "white", bins = 30, binwidth = 1) +
    xlab("Annual Income (Million JPY)") + 
    ylab("Frequency") +
    annotation_custom(grob) +
    annotation_custom(grob_add) +
    theme_bw())

jpeg(file="04_Figure\\11_descriptive_stat.jpeg", 
     width = 297, height = 210, units = "mm", quality = 300, res = 300)
grid.arrange(a, b, c, d,
             nrow = 2)
dev.off()

### importance plot
load("03_Results/01_explainer_data.rf.24.RData")
data.rf.24_aps <- model_parts(explainer_data.rf.24, type = "raw")
test <- data.rf.24_aps
test <- test %>% 
  mutate(
    variable = ifelse(variable == "high_stress", "High-level Stress", variable),
    variable = ifelse(variable == "income_indiv", "Individual Income", variable),
    variable = ifelse(variable == "good_for_living", "Goodness for Living", variable),
    variable = ifelse(variable == "community_attachment", "Community Attachment", variable),
    variable = ifelse(variable == "self_reported_health", "Self-reported Health", variable),
    variable = ifelse(variable == "age", "Age", variable),
    variable = ifelse(variable == "NTL_log", "Logarithm of NTL", variable),
    variable = ifelse(variable == "NDVI", "NDVI", variable),
    variable = ifelse(variable == "low_stress", "Low-level Stress", variable),
    variable = ifelse(variable == "female", "Female Dummy", variable),
    variable = ifelse(variable == "living_environment_satefy", "Safe Feeling of Living Environments", variable),
    variable = ifelse(variable == "bachelor", "Bachelor Dummy", variable),
    variable = ifelse(variable == "worker", "Worker Dummy", variable),
    variable = ifelse(variable == "college_no_diploma", "College without Diploma Dummy", variable),
    variable = ifelse(variable == "housewife", "Housewife Dummy", variable),
    variable = ifelse(variable == "unemployed", "Unemployed Dummy", variable),
    variable = ifelse(variable == "self_employed", "Self-employed Dummy", variable),
    variable = ifelse(variable == "government_officer", "Government Officer Dummy", variable),
    variable = ifelse(variable == "retired", "Retired Dummy", variable),
    variable = ifelse(variable == "master", "Master Dummy", variable),
    variable = ifelse(variable == "company_owner", "Company Owner Dummy", variable),
    variable = ifelse(variable == "professional", "Professional Job Dummy", variable),
    variable = ifelse(variable == "student", "Student Dummy", variable),
    variable = ifelse(variable == "phd", "PhD Dummy", variable),
    variable = ifelse(variable == "overall_LS", "LS", variable)
  )
jpeg(file="04_Figure/importance.jpeg", width = 297, height = 210, units = "mm", quality = 300, res = 300)
plot(test, bar_width = 6, subtitle = "Results of the Random Forest")
dev.off()

result <- plot(test, bar_width = 6, subtitle = "Results of the Random Forest")
result$data %>% View()

###### summary table
load("01_Data/06_dataset.rf24.RData")
stargazer(dataset_used.rf,  
          title = "Table S1: Descriptive Statistics of Features", type = "text", no.space = T,
          covariate.labels = c('LS','Safe Feeling of Living Environments',
                               'Sense of Goodness for Living', 'Community Attachment',
                               'Frequency of High-level Stress', 'Frequency of Low-level Stress',
                               'Female Dummy (Gender)', "Age", "Self-reported Health",
                               "Annually Individual Income (Million JPY)", "College without Diploma",
                               "Bachelor Dummy", 'Master Dummy', "PhD Dummy",
                               "NDVI (%)", "Logarithm of NTL", 
                               'Student Dummy',
                               'Worker Dummy', 'Company Owner Dummy',
                               'Government Officer Dummy',
                               'Self-employed Dummy', "Professional Job Dummy", 
                               'Housewife Dummy', 'Retired Dummy',
                               'Unemployed Dummy'
          ),
          out = '03_Results\\summary.html'
)


##### merge 08 09 10
load("03_Results/03_data.rf.24.PDP.NDVI.RData")
(NDVI.line.pdp <- 
    ggplot(pdp.rf24.NDVI) +
    geom_line( aes(x = V2, y = result), alpha = 0.5, color = "green3", size  = 1) +
    scale_x_continuous(name = "NDVI (%)") +
    scale_y_continuous(name = "LS Prediction - PDP") +
    theme_bw() +
    annotate("text", x = 6, y = 3.39, label = 'bold("a")', parse = TRUE, size = 5))


load("03_Results/04_data.rf.24.PDP.NTL.RData")
(NTL.line.pdp <- 
    ggplot(pdp.rf24.NTL_log, aes(x = V2, y = result)) +
    geom_line(alpha = 0.5, color = "chocolate1", size  = 1) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - PDP") +
    theme_bw() +
    annotate("text", x = 0, y = 3.42, label = 'bold("b")', parse = TRUE, size = 5))

load("03_Results/05_data.rf.24.PDP.income.RData")
(income.line.pdp <- 
    ggplot(pdp.income.df, aes(x = V2, y = result)) +
    geom_line(alpha = 0.5, color = "magenta3", size  = 1) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - PDP") +
    theme_bw() +
    annotate("text", x = 0, y = 3.7, label = 'bold("c")', parse = TRUE, size = 5))

load("03_Results/06_ALE.2.rf24.NDVI.NTL.only.500.RData")
(NDVI.line.ale <- 
    ggplot() +
    geom_line( aes(x = ALE.2.rf24.NDVI.only$x.values, y = ALE.2.rf24.NDVI.only$f.values),
               alpha = 0.5, color = "green3", size  = 1) +
    scale_x_continuous(name = "NDVI (%)") +
    scale_y_continuous(name = "LS Prediction - ALE") +
    theme_bw() +
    annotate("text", x = 6, y = 0.06, label = 'bold("d")', parse = TRUE, size = 5))

(NTL.line.ale <- 
    ggplot() +
    geom_line(aes(x = ALE.2.rf24.NTL.only$x.values, y = ALE.2.rf24.NTL.only$f.values),
              alpha = 0.5, color = "chocolate1", size  = 1) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - ALE") +
    theme_bw() +
    annotate("text", x = 0, y = 0.09, label = 'bold("e")', parse = TRUE, size = 5))

(income.line.ale <- 
    ggplot() +
    geom_line(aes(x = ALE.2.rf24.income.only$x.values, y = ALE.2.rf24.income.only$f.values),
              alpha = 0.5, color = "magenta3", size  = 1) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - ALE") +
    theme_bw() +
    annotate("text", x = 0, y = 0.4, label = 'bold("f")', parse = TRUE, size = 5))

load("03_Results/10_Pseudo.funciton.ALE.RData")
(Fuction.NDVI.line.ale <- 
    ggplot(pred.ALE.NDVI.only[[1]], aes(x = NDVI)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "green3",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "NDVI (%)") +
    scale_y_continuous(name = "LS Prediction - PALEF") +
    theme_bw() +
    annotate("text", x = 6, y = 0.06, label = 'bold("g")', parse = TRUE, size = 5) +
    annotate("text", x = 21, y = -0.075, label = 'bold("R2 = 98.15%")', parse = TRUE, size = 5))

(Fuction.NTL.line.ale <- 
    ggplot(pred.ALE.NTL.only[[1]], aes(x = NTL)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "chocolate1",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "Logarithm of NTL") +
    scale_y_continuous(name = NULL) + # "LS Prediction - PALEF") +
    theme_bw() +
    annotate("text", x = 0, y = 0.09, label = 'bold("h")', parse = TRUE, size = 5) +
    annotate("text", x = 0.8, y = -0.25, label = 'bold("R2 = 99.27%")', parse = TRUE, size = 5))

(Fuction.income.line.ale <- 
    ggplot(pred.ALE.income.only[[1]], aes(x = income)) +
    geom_line( aes(y = yhat), color = "grey77",
               alpha = 0.5, size  = 1, show.legend = F) +
    geom_line( aes(y = yhat_pred), color = "magenta3",
               alpha = 0.5, size  = 1, show.legend = F) +
    scale_x_continuous(name = "Income (Million JPY)") +
    scale_y_continuous(name = NULL) + # "LS Prediction - PALEF") +
    theme_bw() +
    annotate("text", x = 0, y = 0.4, label = 'bold("i")', parse = TRUE, size = 5) +
    annotate("text", x = 25, y = -0.12, label = 'bold("R2 = 99.53%")', parse = TRUE, size = 5))

jpeg(file = "04_Figure/13_mergedFigure.jpeg", width = 297, height = 210,
     units = "mm", quality = 300, res = 300)
grid.arrange(
  NDVI.line.pdp, NTL.line.pdp, income.line.pdp,
  NDVI.line.ale, NTL.line.ale, income.line.ale,
  Fuction.NDVI.line.ale, Fuction.NTL.line.ale, Fuction.income.line.ale,
  nrow = 3)
dev.off()

