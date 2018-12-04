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

Let $U$ the set of all users registered in ROS Answers, $Q$ the set of all questions posted in ROS Answers, we define the relationshio between a user $u \in U$ and a question $q \in Q$ as:

$$ R_{uq}(u,q) = \dfrac{Activity(u,q)}{\sum_{i=1}^{|U_q|} Activity(U_q[i],q)}, \quad U_q = \{u \in U, Activity(u,q)>0\} $$ 

We can see that $\sum_{i=1}^{|U_q|} Activity(U_q[i],q)$ is the sum of comments, answers + 1 (the activity of having published the question). 

We define also the relationshio between two users $a, b \in U$ as:

$$R_{uu}(a,b) = \dfrac{\sum_{q \in Q_a \cap Q_b} R_{uq}(a,q) \cdot R_{uq}(b,q) }{\sqrt{\sum_{q \in Q_a} R_{uq}(a,q)^2 \cdot \sum_{q \in Q_b} R_{uq}(b,q)^2}}$$ 

$$Q_a = \{q \in Q, Activity(a,q) > 0\}, \quad Q_b = \{q \in Q, Activity(b,q) > 0\}$$

The score for a candidate $a$ for participating in question $q$ is:

$$wcfa\_score(a,q) = \sum_{u \in U_q}  R_{uq}(u,q) \cdot R_{uu}(a,u)$$

### How to run

```python
from src/algorithms/weighted_collaborative_filtering_algorithm import WCFAlgorithm

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

As there is no previous activity, this approach is content based. It makes use of the tags that are associated to users and questions. Let $T$ be the set of all tags defined in ROS Answers, $Q_t$ the set of all questions tagged under the $t$ tag, and $T_{uq}$ the set of all tags that match the user $u$ and the question $q$. 

We define the relationship between a user $u$ and a tag $t$ : 

$$ R_{ut}(u,t) = \sum_{q \in Q_t} R_{uq}(u,q) \cdot log \dfrac{|\bigcup_{x \in T} Q_x|}{|Q_t|} $$

And the score for a candidate $a$ for participating in a question $q$ is:

$$tmba\_score(a,q) = |T_{uq}| \cdot  \sum_{t \in T_{uq}} R_{ut}(u,t)$$ 



Our focus should be on the TMBA approach which is when a questions hasn't any activity.

Considerations for improving TMBA approach:

1. Ponderation for tags: users have a counter for tags (ej: Turtlebot x 45, Kinetic x 20, Navigation x 5, etc.). Currently are not making use of it, it's information we are ignoring
2. Questions may be better described if we consider the tags present in their title and body
3. Users can be also be better profiled considering tags in the repositories they participate and their activity on them: e.g. commiting into kinetic branches may increase its counter for *kinetic* tag, a high number of commits in launchfiles may increase the counter for *launch*, *configuration* and *deployment* tags, etc.

```python
from src/algorithms/tag_map_based_algorithm import TMBAlgorithm

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

The score for a candidate $a$ for participating in question $q$ is:

$$c2aa\_score(a,q) = R_{uu}(a,\textrm{asker})$$

```python
from src/algorithms/closeness_to_asker_algorithm import C2AAlgorithm

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

$$ \textrm{# accepted answers} \cdot ( \textrm{# up votes} - \textrm{# down votes} ) $$

The list of the first 150 users sorted by the pseudokarma was got with this query:

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
