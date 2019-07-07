# Data	

## Databases (`v1.db`, `v1.2.db`)

Dump of data from ROS Answers:

- ros_user (in v1.2 includes karma, location, avatar)
- ros_answer
- ros_question
- ros_question_answer
- ros_tag
- ros_user_tag
- ros_question_tag
- linked_users (v1.2)
- linked_tag_project



## Results of experiments

#### Raw Results

The results of the experiment for each question are in a JSON files contained in a directory named by the recommendation approach (wcfa, tmba, c2aa, rpk) and the sample. The  follows the format:`{size_of_the_sample}_{nb_of_participants_in_the_sample}`. 

By December 8th of 2018, The only sample we have used has 100 questions of 5 participants: `100q_5p`. in the following format: `results_for_{question_id}.json`. 

The result for each experiment is named as: `results_for_{question_id}.json`, and it contains a collection of pairs: `[user_id, score]` ordered by score in descending order.

Example, `tmba_100q_1p/results_for_12342.json`:

 `[[121, 17.053305203557994], [11, 11.126979281754151], [12, 9.675634158047089], [8681, 6.143276141934113], ...`

#### Summary of Results: Recall Metric

It also contains one file of a summary of the whole experiment with the **recall metric** for the top 5, top 10, ..., top 150 users, i.e. *how many actual participants from the question are included in the top **n** results*. The file has the format: `results_{wcfa/tmba/c2aa/rpk}_{name_of_the_question_sample}.csv`. 



##  Table of values for <img src="/data/tex/ea37d88a00ab281cc5cbb427cdd39647.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=26.69146424999999pt height=22.465723500000017pt/> (WCFA/C2AA)

For running the experiment calculating the scores with WCFA, it is needed to caculate the value of <p align="center"><img src="/data/tex/0027739b80f8037af689cdd8a47b0197.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=26.69146425pt height=15.936036599999998pt/></p> between a ROS Answers' *user* and a *question*. 

The formula for it is:

<p align="center"><img src="/data/tex/e3ce2458de5775d451aea4363c4a132c.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=512.15675115pt height=43.8784632pt/></p> 

We calculated the values of <p align="center"><img src="/data/tex/0027739b80f8037af689cdd8a47b0197.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=26.69146425pt height=15.936036599999998pt/></p> for all questions and their participants each question and stored them into two files: ``r_uq.json`` and ``r_uq_compact.json``

#### ``r_uq.json``

```json
 {
   "9033": [		// question id
      {
         "u": 2,	// user_id (participant of question 9033)
         "r": 0.25  // R_uq score
      },
      {
         "u": 3,
         "r": 0.25
      },
      {
         "u": 11,
         "r": 0.25
      },
      {
         "u": 139,
         "r": 0.25
      }
   ],
     ...
 }
     
     
```

#### ``r_uq_compact.json``

```json
{"9033": {"2": 0.25, "3": 0.25, "11": 0.25, "139": 0.25}, "9036": {"2": 0.3333333333333333, "3": 0.3333333333333333, "6791": 0.3333333333333333},  ...

```



## Table of values for <img src="/data/tex/0e2de7efc5cf2a727a377bd5aea6eddd.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=25.219418399999988pt height=22.465723500000017pt/> (TMBA) 

For running the experiment calculating the scores with TMBA, it is needed to caculate the value of <p align="center"><img src="/data/tex/eb36e2faf8f8d9d8b7bf70f6f127df7b.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=25.2194184pt height=13.698590399999999pt/></p> between a ROS Answers' *user* and a *tag*. 

The formula for it is:

<p align="center"><img src="/data/tex/5d0a65fc96e4aa5abc98b8b858aaa1ba.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=293.9047419pt height=46.423454549999995pt/></p>

We calculated the values of <p align="center"><img src="/data/tex/eb36e2faf8f8d9d8b7bf70f6f127df7b.svg?invert_in_darkmode&sanitize=true&sanitize=true" align=middle width=25.2194184pt height=13.698590399999999pt/></p> for all questions and their participants each question and stored them into two files: ``r_ut.json``, ``r_ut_compact.json`` and ``r_ut.csv``

#### ``r_ut.json``

```json
{
   "2": [						// user_id
      {
         "t": 1,				// tag_id
         "r": 95.06460870125298	// r_ut score
      },
      {
         "t": 2,
         "r": 25.974351052187604
      },
      {
         "t": 3,
         "r": 21.01833798895972
      },
      {
         "t": 4,
         "r": 4.6972026328423055
      },
      {
         "t": 5,
         "r": 0
      },
     ...
 }
     
     
```

#### ``r_ut_compact.json``

```json
{"2": {"1": 95.06460870125298, "2": 25.974351052187604, "3": 21.01833798895972, "4": 4.6972026328423055, "5": 0, "6": 11.693046713573722,  ...

```

#### ``r_ut.csv`` (user_id, tag_id, r_ut score)

```tsv
u	t	r
2	1	95.06460870125298
2	2	25.974351052187604
2	3	21.01833798895972
2	4	4.6972026328423055
2	5	0
2	6	11.693046713573722
2	7	10.18102624891754
2	8	6.069718594332738
2	9	0
```



## Samples

### 100q_1p: 100 Questions with only 1 participant

Random sample of 100 questions that have no answer yet.

File: ``questions_with_1_participant.json``

#### 100q_5p: 100 Questions with only 5 participants (asker + 4)

Random sample of 100 questions with 4 answers/comments + the *asking* activity

File: ``questions_with_5_participants.json``



## Karma and PseudoKarma values

### Karma values (``ranking_karma.csv``)

Data gathered from database: v.1.2.db

|  id    |   name    | up_votes  | down_votes   | karma  |
|:----:  |:--------: |:--------: |:----------:  |:-----: |
| 3      | tfoote    | 2938      | 80           | 48115  |
| 5184   | gvdhoorn  | 478       | 15           | 43312  |
| 1034   | ahendrix  | 512       | 104          | 41279  |
| 122    | dornhege  | 1710      | 52           | 29613  |
| 25     | joq       | 3782      | 8            | 24183  |


### Karma values (``ranking_pseudokarma.csv``)

Data gathered from database: v.1.db

| author    | resp_acc  |  id    |   name    | up_votes  | down_votes   | pseudokarma  |
|:------:   |:--------: |:----:  |:--------: |:--------: |:----------:  |:-----------: |
| 3         | 1153      | 3      | tfoote    | 2938      | 80           | 3295274      |
| 25        | 574       | 25     | joq       | 3782      | 8            | 2166276      |
| 122       | 773       | 122    | dornhege  | 1710      | 52           | 1281634      |
| 875       | 226       | 875    | 130s      | 3714      | 19           | 835070       |
| 5184      | 1228      | 5184   | gvdhoorn  | 478       | 15           | 568564       |
| 1034      | 1282      | 1034   | ahendrix  | 512       | 104          | 523056       |
| 21        | 459       | 21     | Lorenz    | 997       | 15           | 450738       |