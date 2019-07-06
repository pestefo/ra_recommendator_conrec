import json

"""
Helpers
"""


def get_data(path_to_file):
    with open (path_to_file) as json_data:
        return json.load (json_data)


def results_dir(scenario, nb_of_participants):
    # For an experiment run on 2019-07-02 at 18:28 for all questions of
    # 5 participants with the scenario A:
    # >> "path_to_results/results/20190702_1828/5p/A/"

    import time
    import os

    path_to_results = "{path_to_results}results/{time}/{participants}p/{scenario}" \
        .format (path_to_results=dp,
                 time=time.strftime ("%Y%m%d_%H%M"),
                 participants=nb_of_participants,
                 scenario=scenario)

    os.makedirs (path_to_results, exist_ok=True)
    return path_to_results


def results_file(question_id, scenario, nb_of_participants):
    return results_dir (scenario, nb_of_participants) + '/results_for_' + str (question_id) + '.json'


"""
Directory preffix
"""

dp = '/home/pestefo/projects/ra_recommendator_conrec/'

"""
Database path
"""

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
user_tags_extended_old = dp + 'data/data_extracted_from_db/ros_user_tag_extended-old.json'
user_full_extended_tags = dp + 'data/tag_extensions/user_full_extended_tags.json'

question_full_extended_tags = dp + 'data/tag_extensions/question_full_extended_tags.json'
full_extended_tags_to_questions = dp + 'data/tag_extensions/full_extended_tags_to_questions.json'
"""
 Question ID - User ID - R_uq calculation
 {"question_id": [ {u": user_id, "r": r_uq_value}, ... ],
"""
r_uq_table = dp + 'data/r_uq.json'

"""
 User ID - Tag ID - R_ut calculation
 {"user_id": [ {t": tag_id, "r": r_ut_value}, ... ],
"""
r_ut_table = dp + 'data/r_ut.json'
r_ut_table_scenario = {
    'A': dp + 'data/r_ut.json',
    'B': dp + 'data/r_ut_scenario_b.json',
    'C': dp + 'data/r_ut_scenario_c.json',
    'D': dp + 'data/r_ut_scenario_d.json'
}

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

tables = dp + 'data/table_and_column_names.json'

questions_sample_100q_5p = dp + 'data/list_of_questions_with_5_participants.json'

"""
Stopwords for ExtendedTagExtractor
"""
stopwords = [dp + 'src/utils/stopwords.txt', dp + 'src/utils/stopwords-complement.txt']

"""
Data for testing
"""
tag_data_for_testing = get_data (dp + 'data/test_data/tags_data.json')
