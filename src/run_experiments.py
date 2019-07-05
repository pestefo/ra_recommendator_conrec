#!/usr/bin/env python
# coding: utf-8

'''
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm
from algorithms.tag_map_based_algorithm import TMBAlgorithm
from algorithms.closeness_to_asker_algorithm import C2AAlgorithm
'''
import datetime
import json
import sys
import time

from src.algorithms.tag_map_based_algorithm import TMBAlgorithm
from src.utils import data_files as files
from src.utils.db import Database

# path_to_results = 'data/tmba_100q_5p'

# path_to_results = 'data/tmba_100q_1p'
# sample_file_path = 'data/questions_with_1_participant.json'
# path_to_results = 'data/wcfa_100q_5p_2nd_exp'

"""
Specs: algorithm, sample_size, nb_results, scenarios
"""
spec = {
    "ALGORITHM": None,
    "SAMPLE_SIZE": 100,
    "NB_OF_PARTICIPANTS": 5,
    "NB_OF_RESULTS": 100,
    "SCENARIOS": ('A', 'B', 'C', 'D'),
}

"""
Utils
"""


def print_header(question_id, scenario):
    global spec
    print ("------- start (Scenario {} - {} participants ) -------".format (scenario, spec['NB_OF_PARTICIPANTS']))
    print ("question: " + str (question_id))
    now = datetime.datetime.now ()
    print (now.strftime ('%d-%m-%Y %H:%M:%S'))
    return now


def print_footer(start_time, now):
    print ("\n" + str ((datetime.datetime.now () - now).seconds) + " seconds")
    print (time.strftime ('%H:%M:%S',
                          time.gmtime ((
                                               datetime.datetime.now () - start_time)
                                       .seconds)) +
           " elapsed.")
    print ("------- end -------\n\n")


def run_experiment(question_id, filename):
    global spec
    with open (filename, 'w') as write_file:
        results = spec['ALGORITHM'].ranking_for_question (question_id,
                                                          spec['NB_OF_RESULTS'])
        json.dump (results, write_file)


def get_sample(nb_of_participants, limit_size=None, dummy_sample=None):
    if dummy_sample:
        return sample_100q_5p ()

    db = Database ('A')  # we don't really make use of scenarios-specific methods
    sample = db.questions_with_n_participants (nb_of_participants)

    if limit_size:
        return sample[:limit_size]

    return sample


def sample_100q_5p():
    # Special sample that i've been using for testing the algorithms
    # There are 100 questions with 5 participants (1 asker + 4 answerers
    # or commenters
    return files.get_data (files.questions_sample_100q_5p)[:100]


"""
For each scenario (A, B, C and D) runs the experiment
with the given specifications: paths to leave the results,
sample (described by number of participants), number of results.
"""


def main():
    global spec

    # specifying sample from command line
    if sys.argv[1]:
        spec['NB_OF_PARTICIPANTS'] = sys.argv[1]

    # Get sample of questions
    spec['SAMPLE'] = get_sample (spec['NB_OF_PARTICIPANTS'], dummy_sample=True)  # 100q_5p sample
    # spec['SAMPLE'] = get_sample (spec['NB_OF_PARTICIPANTS'])

    # Start clicking
    start_time = datetime.datetime.now ()

    # for scenario in SCENARIOS:
    for scenario in spec['SCENARIOS']:
        spec['ALGORITHM'] = TMBAlgorithm (scenario)
        # spec['ALGORITHM'] = MockRanking ()

        # Run experiment for each question in the sample
        for question_id in spec['SAMPLE'][: spec['SAMPLE_SIZE']]:
            now = print_header (question_id, scenario)

            filename = files.results_file (question_id, scenario, spec['NB_OF_PARTICIPANTS'])

            # Process and write results
            run_experiment (question_id, filename)

            print_footer (start_time, now)


if __name__ == '__main__':
    main ()
