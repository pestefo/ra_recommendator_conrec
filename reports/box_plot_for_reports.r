library(ggplot2)
library(readr)
require(reshape2)


#data <- read.delim("~/projects/experiment_1/data/wcfa_100q_5p_2nd_exp/results_wcfa_100q_5p_2nd_exp.csv")
#data <- read.delim("~/projects/experiment_1/data/wcfa_100q_5p/results_wcfa_100q_5p.csv")
#data <- read.delim("~/projects/experiment_1/data/tmba_100q_5p/results_tbma_100q_5p.csv")
#data <- read.delim("~/projects/experiment_1/data/tmba_100q_1p/results_tmba_100q_1p.csv")
data <- read.delim("/home/pestefo/projects/ra_recommendator_conrec/results/second_experiments/scenario_A/results_scenario_A.csv")

n_part <- '5'

ggplot(data = melt(data[1:length(data)],id='q_id'), aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=variable), fill='white', color="black") + 
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  labs(x = "Recall on the first 150 results") +
  labs(y = "recall") +
  labs(title = "Scenario A: Q - U / Recall on 100 questions of 5 participants per question")

  
