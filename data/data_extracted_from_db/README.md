# Data extracted from DB

## Tables (CSV)

There following files are a simple CSV file generated through a  ``select * from {table}``:

| table               | header                        | file                        |
| ------------------- | ----------------------------- | --------------------------- |
| ros_answer          | no header                     | ``ros_answer.csv``          |
| ros_question        | no header                     | ``ros_question.csv``        |
| ros_question_answer | ros_question_id,ros_answer_id | ``ros_question_answer.csv`` |
| ros_question_tag    | ros_question_id,ros_tag_id    | ``ros_question_tag.csv``    |
| ros_tag             | id,name                       | ``ros_tag.csv``             |
| ros_user            | no header                     | ``ros_user.csv``            |
| ros_user_tag        | ros_user_id,ros_tag_id,count  | ``ros_user_tag.csv``        |

## JSON files

### Dictionary ``ros_tag_name_dictionary.json``

The JSON file ``ros_tag_name_dictionary.json``is a dictionary of the tag names for each tag id: ``tag_id --> tag_name``

```json
{"1": "turtlebot", "2": "Kinect", "3": "gyro", "4": "gmapping", "5": "turtlebot_dash...", "6": "rviz", "7": "irobot_create", ...
```



### Dictionary   ``ros_user_tag.json``  

The JSON file ``ros_user_tag.json`` is a dictionary of the *tags* associated to a *user* and its count: ``user_id --> [ tag_id, count ]``. For example, in the following extract there are all the tags associated to ``user_id = 2``: ``tag_id = 1``has ``count = 1``, ``tag_id = 4`` has a ``count = 19``, etc.

```json
{"2": [{"tag": "1", "count": "150"}, {"tag": "2", "count": "43"}, {"tag": "3", "count": "20"}, {"tag": "4", "count": "19"}, ...
```

### Dictionary ``ros_question_tag.json``

The JSON file ``ros_question_tag.json`` is a dictionary of the *tags* associated to a *question* and its count: ``question_id --> [ tag_1, tag_2, ... , tag_n ]``.

```json
{"9033": ["37", "123"], "9036": ["17", "20", "22"], "9037": ["17", "20", "39"],
```

