

"""
Directory preffix
"""

# dir_preffix = '/home/pestefo/projects/experiment_1/'
dir_preffix = '/home/pestefo/projects/ra_recommendator_conrec/'

db_file = dir_preffix + 'data/v1.2.db'

"""
 User ID - Tag ID - Count
 {"user_id": [{"tag": "tag_id", "count": "count_record"}, ...
"""
user_tags_file = dir_preffix + 'data/data_extracted_from_db/ros_user_tag.json'

"""
 User ID - Tag ID
 {"user_id": ["tag_1", "tag_2", "tag_3".  ...], "another_user_id" : [...]

 Extracted from the questions in which the user has participated
 and the extended tag description
"""
user_tags_extended_file = None

"""
 User ID - Tag ID - R_ut calculation
 {"user_id": [ {t": tag_id, "r": r_ut_number}, ... ],
"""
r_ut_table_file = dir_preffix + 'data/r_ut.json'

"""
 Question ID - List of Tag IDs
 {"9033": ["37", "123"], "9036": ["17", "20", "22"],
"""
question_tags_file = dir_preffix + \
    'data/data_extracted_from_db/ros_question_tag.json'

"""
Question ID - List of Tag IDs  -    Considering manually entered and
                                    and extracted from body and title
"""
question_tags_extended_file = dir_preffix + \
    'data/ros_question_tag_extended.json'
tags_file = dir_preffix + 'data/data_extracted_from_db/ros_tag.json'
