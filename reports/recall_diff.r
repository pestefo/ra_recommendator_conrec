# Getting data
library(dplyr)
recall_data_for_scenario <- function(scenario) {
  path_preffix <- "/home/pestefo/projects/ra_recommendator_conrec/results/second_experiments/scenario_"
  read.delim(paste(path_preffix,scenario,"/results_scenario_",scenario,".csv",sep=""))  
}

recall_A <- recall_data_for_scenario('A')
recall_B <- recall_data_for_scenario('B')
recall_C <- recall_data_for_scenario('C')
recall_D <- recall_data_for_scenario('D')

rownames(recall_A) <- recall_A$q_id
rownames(recall_B) <- recall_B$q_id
rownames(recall_C) <- recall_C$q_id
rownames(recall_D) <- recall_D$q_id


# Absolute Value of Delta between Recall(Baseline) and Recall(Other Scenario)
# data = data.frame(colSums(abs(recall_A - recall_B)[-1]), colSums(abs(recall_A - recall_C)[-1]), colSums(abs(recall_A - recall_D)[-1] ) )

# Delta between Recall(Baseline) and Recall(Other Scenario)
# data = data.frame(colSums(recall_A - recall_B)[-1], colSums(recall_A - recall_C)[-1], colSums(recall_A - recall_D)[-1]  )

# Cumulative Recall
# data = data.frame(colSums(recall_A[-1]),colSums(recall_B[-1]),colSums(recall_C[-1]),colSums(recall_D[-1])) 

# Headers for Data and Writing
# colnames(data) <- c("Recall(B - A)", 	"Recall(C - A)" ,	"Recall(D - A)")
# write.table(data, "./delta_of_recalls.csv", sep="\t")



