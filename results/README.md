# Results

## First experiments: WCFA/C2AA/TMBA/Karma

Initial exploratory experiments for testing WCFA, TMBA, C2AA against the RPK (baseline).

| Method | Nb of Questions | Nb of Participants    | Folder                                                       | Observations                                                 |
| ------ | --------------- | --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| WCFA   | 100             | 1 asker + 4 answerers | [`wcfa_100q_5p`](../results/first_experiments/wcfa_100q_5p)  | See [the results](../reports/wcfa_100q_5p.pdf).              |
| C2AA   | 100             | 1 asker + 4 answerers | [`wcfa_100q_5p_4hidden`](../results/first_experiments/wcfa_100q_5p_4hidden/) | This method is the same as WCFA but for R_uu there is no knowledge about participation in the target question. See [the results](../reports/wcfa_100q_5p_4hidden.pdf). |
| TMBA   | 100             | 1 asker + 4 answerers | [`tmba_100q_5p`](../results/first_experiments/tmba_100q_5p/) | See [the results](../reports/tmba:100q_5p.pdf).              |
| TMBA   | 100             | 1 asker + 0 answerers | [`tmba_100q_1p`](../results/first_experiments/tmba_100q_1p/) | TMBA for the COLD START problem. See [the results](../reports/tmba_100q_1p.pdf). |
| RPK    | 100             | 1 asker + 4 answerers | [`rpk_100p_5p`]((../results/first_experiments/rpk_100q_5p/)) | PseudoKarma. See [the results](../reports/rpk_100q_5p.pdf).  |



## Second experiments (TMBA): using extended tag description of questions and users

#### Objective

To determine if describing questions and/or users with the tags in the body and title of questions can improve the behaviour of TMBA.

#### Scenarios 

A. **Baseline**: no use of extended tag description
B. **Questions extended** tag description but Users non-extended
C. Questions non-extended and **Users extended** tag description
D. **Questions extended** tag description - **Users extended** tag description

### Tasks

- [x] Extract new tags from Questions: generate `ros_question_tag_extended.json`
- [x] Extract new tags from participation of Users in Questions: generate `ros_user_tag_extended.json` --> (`ra_user_tag_extended` in the DB)
- [ ] Generate R_ut for Scenario B: generate `r_ut_scenario_b.json`
- [ ] Generate R_ut for Scenario C: generate `r_ut_scenario_c.json`
- [ ] Generate R_ut for Scenario D: generate `r_ut_scenario_d.json`
- [ ] Get scores for Scenario B
- [ ] Get scores for Scenario C
- [ ] Get scores for Scenario D
- [ ] Overall evaluation for Scenario B (boxplot of recall)
- [ ] Overall evaluation for Scenario C (boxplot of recall)
- [ ] Overall evaluation for Scenario D (boxplot of recall)
- [ ] Manual inspection



  