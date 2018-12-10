# ra_recommendator_conrec
*Adaptation of ConRec for ROS Answers' Answerers Recommendation*

ConRec is a recommender of developer candidates (technically a GitHub users) for a target software project (technically a GitHub repository). 

#### Concepts equivalence between the original and the adaptation

GH = GitHub, RA = ROS Answers

1. GH Project <—> RA Question
2. GH User <—> RA  User
3. \# Commit <—> # Activity := # of comments/answers + 1 (if asked the target question)

Ej. If *a* asks *q* and leaves two comments, #Activity(*a*) = 2 + 1 = 3, for any other user, #Activity will consider having commented or asked only.

ConRec works in two different ways regarding the question has or not previous activity. 

A. **Not Cold Start**: There is any comment or answer to the question. In this case *ConRec* applies the **Weighted Collaborative Filtering Algorithm (WCFA)**

B. **Cold Start**: There is not activity in the questions besides its publication. In this case *ConRec* applies the **Tag Map Based Algorithm**. 

## Weighted Collaborative Filtering Algorithm (WCFA)

Let <img src="/tex/6bac6ec50c01592407695ef84f457232.svg?invert_in_darkmode&sanitize=true" align=middle width=13.01596064999999pt height=22.465723500000017pt/> the set of all users registered in ROS Answers, <img src="/tex/1afcdb0f704394b16fe85fb40c45ca7a.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=22.465723500000017pt/> the set of all questions posted in ROS Answers, we define the relationshio between a user <img src="/tex/b99229d16d8abc14e14acbb99bbccfae.svg?invert_in_darkmode&sanitize=true" align=middle width=42.51737159999999pt height=22.465723500000017pt/> and a question <img src="/tex/15e1f565287c20880b8df7292f1755b9.svg?invert_in_darkmode&sanitize=true" align=middle width=41.01465059999999pt height=22.465723500000017pt/> as:

<p align="center"><img src="/tex/e3ce2458de5775d451aea4363c4a132c.svg?invert_in_darkmode&sanitize=true" align=middle width=512.15675115pt height=43.8784632pt/></p> 

We can see that <img src="/tex/e3a4d206f15d05ffe567fd31f7d89594.svg?invert_in_darkmode&sanitize=true" align=middle width=165.35567894999997pt height=35.06841029999999pt/> is the sum of comments, answers + 1 (the activity of having published the question). 

We define also the relationshio between two users <img src="/tex/0985970f68fecf6dbb54faa79ec8ad4b.svg?invert_in_darkmode&sanitize=true" align=middle width=56.15693324999999pt height=22.831056599999986pt/> as:

<p align="center"><img src="/tex/80dfc61617c6bb214d6937634ecbb887.svg?invert_in_darkmode&sanitize=true" align=middle width=364.78036319999995pt height=54.3471885pt/></p> 

<p align="center"><img src="/tex/bae510edcde4971e8ed1932fbfa71c54.svg?invert_in_darkmode&sanitize=true" align=middle width=489.39634259999997pt height=16.438356pt/></p>

The score for a candidate <img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/> for participating in question <img src="/tex/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode&sanitize=true" align=middle width=7.928106449999989pt height=14.15524440000002pt/> is:

<p align="center"><img src="/tex/27bf870bb72dd0ab7cded20720e5ef33.svg?invert_in_darkmode&sanitize=true" align=middle width=319.40076465pt height=40.14634635pt/></p>

### How to run

```python
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm

w = WCFAlgorithm()

# Candidate user
candiate_id = 7

# Target question
question_id = 9045

# Get the score of user 7 for question 9045
w.score(candidate_id,question_id)

# Get a list of top 100 users recommended for question 9045
w.ranking(9045,100)

```


## Tag Map Based Algorithm (TBMA)

As there is no previous activity, this approach is content based. It makes use of the tags that are associated to users and questions. Let <img src="/tex/2f118ee06d05f3c2d98361d9c30e38ce.svg?invert_in_darkmode&sanitize=true" align=middle width=11.889314249999991pt height=22.465723500000017pt/> be the set of all tags defined in ROS Answers, <img src="/tex/025b11cd28d6c936d3062a554bbaf0b5.svg?invert_in_darkmode&sanitize=true" align=middle width=17.96121689999999pt height=22.465723500000017pt/> the set of all questions tagged under the <img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/> tag, and <img src="/tex/ca3b1156ca87c35b6cf1b4ab852bf22a.svg?invert_in_darkmode&sanitize=true" align=middle width=23.81617589999999pt height=22.465723500000017pt/> the set of all tags that match the user <img src="/tex/6dbb78540bd76da3f1625782d42d6d16.svg?invert_in_darkmode&sanitize=true" align=middle width=9.41027339999999pt height=14.15524440000002pt/> and the question <img src="/tex/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode&sanitize=true" align=middle width=7.928106449999989pt height=14.15524440000002pt/>. 

We define the relationship between a user <img src="/tex/6dbb78540bd76da3f1625782d42d6d16.svg?invert_in_darkmode&sanitize=true" align=middle width=9.41027339999999pt height=14.15524440000002pt/> and a tag <img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/> : 

<p align="center"><img src="/tex/5d0a65fc96e4aa5abc98b8b858aaa1ba.svg?invert_in_darkmode&sanitize=true" align=middle width=293.9047419pt height=46.423454549999995pt/></p>

And the score for a candidate <img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/> for participating in a question <img src="/tex/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode&sanitize=true" align=middle width=7.928106449999989pt height=14.15524440000002pt/> is:

<p align="center"><img src="/tex/916948e29aad279e074ac5c1fa6a7f92.svg?invert_in_darkmode&sanitize=true" align=middle width=283.9078704pt height=40.14634635pt/></p> 



Our focus should be on the TMBA approach which is when a questions hasn't any activity.

Considerations for improving TMBA approach:

1. Ponderation for tags: users have a counter for tags (ej: Turtlebot x 45, Kinetic x 20, Navigation x 5, etc.). Currently are not making use of it, it's information we are ignoring
2. Questions may be better described if we consider the tags present in their title and body
3. Users can be also be better profiled considering tags in the repositories they participate and their activity on them: e.g. commiting into kinetic branches may increase its counter for *kinetic* tag, a high number of commits in launchfiles may increase the counter for *launch*, *configuration* and *deployment* tags, etc.

```python
from algorithms.tag_map_based_algorithm import TMBAlgorithm

t = TMBAlgorithm()

# Candidate user
candiate_id = 7

# Target question
question_id = 9045

# Get the score of user 7 for question 9045
t.score(candidate_id,question_id)

# Get a list of top 100 users recommended for question 9045
t.ranking(9045,100)
```


## Closeness to Asker Algorithm (C2AA)

This approach is similar to the Weighted Collaborative Filtering Algorithm, but it works forcing a _Cold Start_ 
situation: the score of the candidate is weithed by the relationship between he/she and the asker only. 
In the case of a question without answers it works exactly as WCFA. 

The score for a candidate <img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/> for participating in question <img src="/tex/d5c18a8ca1894fd3a7d25f242cbe8890.svg?invert_in_darkmode&sanitize=true" align=middle width=7.928106449999989pt height=14.15524440000002pt/> is:

<p align="center"><img src="/tex/5b7bf3d2d9282da74efab5638ece68b9.svg?invert_in_darkmode&sanitize=true" align=middle width=250.57815915pt height=16.438356pt/></p>

```python
from algorithms.closeness_to_asker_algorithm import C2AAlgorithm

c = C2AAlgorithm()

# Candidate user
candiate_id = 7

# Target question
question_id = 9045

# Get the score of user 7 for question 9045
c.score(candidate_id,question_id)

# Get a list of top 100 users recommended for question 9045
c.ranking(9045,100)
```

## Ranking by (Pseudo)Karma (RPK)

The probably simplest approach to obtain a list of recommended users to answer
a question is to go to the [user's list](http://answers.ros.org/users) and contact
users according to their karma level (they are sorted by their karma/reputation points).
The karma system is based on the up/down votes of a user and it's accepted answers.
It is calculated regarding also the historical activity of a user (there are day limit point
increments), then with the data we have (answers, accepted answers, up votes, down votes) we
can only get an approximation of it.
The pseudo-karma is calculated by:

<p align="center"><img src="/tex/a99d36616a4cc4420eec02dd20e9f2f1.svg?invert_in_darkmode&sanitize=true" align=middle width=319.13252745pt height=16.438356pt/></p>

The list of the first 150 users sorted by the *pseudokarma* was got with this query:

```sqlite
select *, 
       ( up_votes - down_votes ) * resp_acc as pseudokarma 
from   (select author, 
               Count(*) as resp_acc 
        from   ros_answer 
        where  is_accepted = 1 /*type='answer'*/ 
        group  by author 
        order  by resp_acc desc) as A 
       join ros_user 
         on ros_user.id = A.author 
order  by pseudokarma desc 
limit  150 

```

## Ranking by Karma (RK)

The v1.2 of the dump from ROS Answers includes the information regarding the karma score of users.

The list of the first 150 users sorted by the *karma* was got with this query:

```sqlite
select id, name, karma, up_votes, down_votes
from ros_user 
order by karma desc
limit 150
```



## Implementation Notes

### Table for Activity

#### Answering and commenting
```sqlite
-- Activity: answering or commenting
select q_id, u_id, count(*) as activity
from
(
	select rqa.ros_question_id as q_id, ra.author as u_id, ra.type, ra.votes, ra.is_accepted
	from ros_question_answer as rqa
	left join ros_answer as ra on rqa.ros_answer_id = ra.id
)
group by q_id, u_id
```

#### Asking
```sqlite
-- Activity: asking | for each question, activity is one (had asked the question)
select q_id, author, 1 as activity
from 
(
	select distinct ros_question_answer.ros_question_id as q_id
	from ros_question_answer
) as questions
left join ros_question as rq on questions.q_id = rq.id
```

### Table for Answering/Commenting activities for question _q_=9045
```sqlite
select *
from
(
	select rqa.ros_question_id as q_id, ra.author as u_id, ra.type, ra.votes, ra.is_accepted
	from ros_question_answer as rqa
	left join ros_answer as ra on rqa.ros_answer_id = ra.id
)
where q_id = 9045 
```

### Table for Questions in which user _u_=3 has participated

```sqlite
select distinct rqa.ros_question_id 
from 
(
	select *
	from ros_answer
	where author = 3
) as ra
left join ros_question_answer as rqa 
	on ra.id = rqa.ros_answer_id
```

### Table for Questions asked by _u_=3 and there's been any participation
```sqlite
select distinct rqa.ros_question_id 
from 
(
	select *
	from ros_question
	where author = 3
) as rq
left join ros_question_answer as rqa on rq.id = rqa.ros_question_id
```

### Table for Question asked by _u_=3
```sqlite
select * 
from ros_question
where author = 3
```
