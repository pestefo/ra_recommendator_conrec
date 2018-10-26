# ra_recommendator_conrec
ConRec implementation for ROS Answers 

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