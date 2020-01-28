# Reports



Here we list all the reports derived from experiment results performed so far:\

### Recall Measurement of TMBA for each scenario and number of participants [VALID]

- Directory: `recall_charts/`
- Notebooks: `Recall After addition of Stopwords - USED IN SAC PAPER.ipynb`
- Status: Used for paper

I plotted boxplots of the recall for TMBA ranking over all questions per scenario (A, B, C and D) and number of participants in questions.

### Analysis of Cases With Low Performance of TMBA per Scenario

- Directory: `analysis_of_cases_of_tmba_with_low_perfomance/`
- Notebooks: `Analysis of Questions with Bad Performance.ipynb`
- Status: Not used

It is expected that recall grows as more users are included in the ranking because the probability of finding participants of such questions grows. 

We wanted to know the effect of addition of stopwords influenced the recall by filtering all the questions in which the recall of TMBA was <= 0.2 at Top 60 users in any Scenario. In other words, if recall@60 is <= 0.2 for any scenario, we included into a list of low performance questions.

For such questions, we compared the improvement or decay of such scenario against baseline. This should answer the question: *Does the addition of tags in Questions and/or Users improved or worsened the performance compared to not having added tags at all?*

We put an up/down arrow mark when the delta of recall in scenarios B, C or D was better/worse than baseline in a minor way (Recall(B/C/D) - Recall(A) <= 0.4). We put two up/down arrows if it was **major** difference comparing to baseline: Recall(B/C/D) - Recall(A) > 0.4. And a dash if there was no difference at all.



### Analysing Karma and TMBA rankings

- Directory: `tmba_vs_karma_ranking_analysis/`
- Notebooks:
  -  `Visualizing Contrast of TMBA vs Karma.ipynb`
  - `Comparing Recommendations against Karma.ipynb`
- Status: Working on it

The second part of the analysis for the study is to analyze how good is TMBA in contrast to a baseline.
We chose the Karma Ranking as a baseline to compare with because is a fair user's ranking (and the only one) provided by ROS Answers. 



### Tag Extension Analysis in TMBA Performance

- Directory: `tag_extension_analysis_in_tmba_performance/`
- Notebooks: `Tag Extension Analysis in TMBA Performance.ipynb`
- Status: Not used

Here we analyzed which tags are involved in questions with good/bad performance with or without extending tags.



### Cummulative Recall and Deltas

- Directory: `cummulative_recall_and_deltas/`
- Notebooks: `recall_diff.r`
- Status: Not used

Cummulative sum of recall through inclusion of more users of ranking per scenario.



### Firsts TMBA vs WCFA recall results (NO LONGER VALID)

- Directory: `firsts_tmba_and_wcfa_recall_results_no_longer_valid/`
- Notebooks: `box_plot_for_reports.r`
- Status: Not valid for current analysis

Boxplots of firsts results when comparing TMBA vs WCFA.

