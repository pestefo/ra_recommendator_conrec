library(ggplot2)
library(readr)
require(reshape2)

prefix = "~/projects/ra_recommendator_conrec/results/20190710_1914_5p/recall_for_scenario_"
scenarios = c("A.csv", "B.csv", "C.csv", "D.csv")

#data <- read.delim("~/projects/experiment_1/data/wcfa_100q_5p_2nd_exp/results_wcfa_100q_5p_2nd_exp.csv")
#data <- read.delim("~/projects/experiment_1/data/wcfa_100q_5p/results_wcfa_100q_5p.csv")
#data <- read.delim("~/projects/experiment_1/data/tmba_100q_5p/results_tbma_100q_5p.csv")
#data <- read.delim("~/projects/experiment_1/data/tmba_100q_1p/results_tmba_100q_1p.csv")

data <- read.delim(paste(prefix,scenarios[1]))


ggplot(data = melt(data[1:length(data)],id='q_id'), aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=variable), fill='white', color="black") + 
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  labs(x = "Recall on the first 150 results") +
  labs(y = "recall") +
  labs(title = "Scenario A: Q - U (both non-extended) / Recall on 100 questions of 5 participants per question")

  
