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

### Table for Answering/Commenting activities for certain question
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


