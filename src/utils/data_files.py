import json

"""
Directory preffix
"""

dp = '/home/pestefo/projects/ra_recommendator_conrec/'

db = dp + 'data/v1.2.db'

"""
 User ID - Tag ID - Count
 {"user_id": [{"tag": "tag_id", "count": "count_record"}, ...
"""
user_tags = dp + 'data/data_extracted_from_db/ros_user_tag.json'

"""
 User ID - Tag ID
 {"user_id": ["tag_1", "tag_2", "tag_3".  ...], "another_user_id" : [...]

 Extracted from the questions in which the user has participated
 and the extended tag description
"""
user_tags_extended = None

"""
 Question ID - User ID - R_uq calculation
 {"question_id": [ {u": user_id, "r": r_uq_value}, ... ],
"""
r_ut_table = dp + 'data/r_uq.json'

"""
 User ID - Tag ID - R_ut calculation
 {"user_id": [ {t": tag_id, "r": r_ut_value}, ... ],
"""
r_ut_table = dp + 'data/r_ut.json'

"""
 Question ID - List of Tag IDs
 {"9033": ["37", "123"], "9036": ["17", "20", "22"],
"""
question_tags = dp + \
    'data/data_extracted_from_db/ros_question_tag.json'

"""
Question ID - List of Tag IDs  -    Considering manually entered and
                                    and extracted from body and title
"""
question_tags_extended = dp + \
    'data/ros_question_tag_extended.json'
tags_file = dp + 'data/data_extracted_from_db/ros_tag.json'


def get_data(path_to_file):
    with open(path_to_file) as json_data:
        return json.load(json_data)
