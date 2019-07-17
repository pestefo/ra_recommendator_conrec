import json
import os

"""
Helpers
"""


def get_data(path_to_file):
    with open(path_to_file) as json_data:
        return json.load(json_data)


def results_dir(date_and_time, nb_of_participants):
    """
    # For an experiment run on 2019-07-02 at 18:28 for all questions of
    5 participants with the scenario A:
    >> "path_to_results/results/20190702_1828/5p/"

    :param date_and_time: it is formatted like this: "%Y%m%d_%H%M", eg.
        an experiment run on 2019-07-02 at 18:28 --> "20190702_1828"
    :type date_and_time: str
    :param nb_of_participants: number of participants in the question
    :type nb_of_participants: int
    :return: full path towards the result files
    :rtype: str
    """

    path_to_results = "{path_to_results}results/{time}_{participants}p" \
        .format(path_to_results=dp,
                time=date_and_time,
                participants=nb_of_participants)

    os.makedirs(path_to_results, exist_ok=True)
    return path_to_results


def path_to_results_of_question(date_and_time, sample, scenario, question_id):
    """
    Example:
    "path_to_results/results/20190702_1828_5p/A/9041.json"

    :param question_id: id of the question
    :type question_id: int
    :param scenario: the scenario where the experiment was performed
    :type scenario: src.algorithms.scenarios.Scenario
    :param sample: to get the nb of participants
    :type sample: src.algorithms.experiment_samples.Sample
    :param date_and_time: it is formatted like this: "%Y%m%d_%H%M", eg.
        an experiment run on 2019-07-02 at 18:28 --> "20190702_1828"
    :return: path to filename of results of the experiment for a question
    :rtype:str
    """
    path_prefix = "{path_to_results}/{scenario}".format(path_to_results=results_dir(date_and_time,
                                                                                    sample.nb_of_participants()),
                                                        scenario=scenario.id())
    os.makedirs(path_prefix, exist_ok=True)
    return "{path}/{q_id}.json".format(path=path_prefix, q_id=question_id)


def filename_of_recall_of_scenario_and_sample(date_and_time, scenario, sample):
    """
    Example:
    "path_to_results/results/20190702_1828_5p/recall_for_scenario_A.csv"

    :param scenario: the scenario where the experiment was performed
    :type scenario: src.algorithms.scenarios.Scenario
    :param sample: to get the nb of participants
    :type sample: src.algorithms.experiment_samples.Sample
    :param date_and_time: it is formatted like this: "%Y%m%d_%H%M", eg.
        an experiment run on 2019-07-02 at 18:28 --> "20190702_1828"
    :return: path to filename of recall results
    :rtype:str
    """
    return "{path_to_results}/recall_for_scenario_{scenario}.csv".format(
            path_to_results=results_dir(date_and_time, sample.nb_of_participants()),
            scenario=scenario.id())


def filename_of_recall_of_scenario_and_nb_of_participants(date_and_time, scenario, nb_of_participants):
    """
    Example:
    "path_to_results/results/20190702_1828_5p/recall_for_scenario_A.csv"

    :param scenario: the scenario where the experiment was performed
    :type scenario: src.algorithms.scenarios.Scenario
    :param nb_of_participants: the nb of participants in that question
    :type nb_of_participants: int
    :param date_and_time: it is formatted like this: "%Y%m%d_%H%M", eg.
        an experiment run on 2019-07-02 at 18:28 --> "20190702_1828"
    :return: path to filename of recall results
    :rtype:str
    """
    return "{path_to_results}/recall_for_scenario_{scenario}.csv".format(
            path_to_results=results_dir(date_and_time, nb_of_participants),
            scenario=scenario.id())


def question_result_files(date_and_time, nb_of_participants, scenario):
    import os

    path = "{prefix_path}/{scenario}".format(prefix_path=results_dir(date_and_time, nb_of_participants),
                                             scenario=scenario.id())

    files_dict = {}
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                q_id = file[:-5] # file = '10130.json' -> q_id = '10130'
                files_dict[q_id] = os.path.join(r, file)
                # files_dict.append(os.path.join(r, file))
    return files_dict


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
r_uq_table_old = dp + 'data/r_uq.json'  # bad format ['question_id' : {'u':user_id, 'r': score} ...
r_uq_table = dp + 'data/r_uq_compact.json'  # good format ['question_id': {'user_id':score, ...}

"""
 User ID - Tag ID - R_ut calculation
 {"user_id": [ {t": tag_id, "r": r_ut_value}, ... ],
"""
r_ut_table = dp + 'data/r_ut.json'
r_ut_table_scenario = {
    'A': dp + 'data/r_ut/scenario_a.json',
    'B': dp + 'data/r_ut/scenario_b.json',
    'C': dp + 'data/r_ut/scenario_c.json',
    'D': dp + 'data/r_ut/scenario_d.json'
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
# tag_data_for_testing = get_data (dp + 'data/test_data/tags_data.json')
