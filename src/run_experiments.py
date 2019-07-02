#!/usr/bin/env python
# coding: utf-8

'''
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm
from algorithms.tag_map_based_algorithm import TMBAlgorithm
from algorithms.closeness_to_asker_algorithm import C2AAlgorithm
'''
from src.algorithms.tag_map_based_algorithm import TMBAlgorithm
from src.utils import data_files as files
import json
import datetime
import time

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
    "NB_OF_PARTICIPANTS": None,
    "NAME_OF_SAMPLE": None,
    "NB_OF_RESULTS": 100,
    "SCENARIOS": ('A', 'B', 'C', 'D'),
}

"""
Utils
"""


def print_header(question_id, scenario):
    print("------- start (Scenario {}) -------".format(scenario))
    print("question: " + str(question_id))
    now = datetime.datetime.now()
    print(now.strftime('%d-%m-%Y %H:%M:%S'))
    return now


def print_footer(start_time, now):
    print("\n" + str((datetime.datetime.now() - now).seconds) + " seconds")
    print(time.strftime('%H:%M:%S',
                        time.gmtime((
                                            datetime.datetime.now () - start_time)
                                    .seconds)) +
          " elapsed.")
    print("------- end -------\n\n")


def run_experiment(question_id, filename):
    global spec
    with open(filename, 'w') as write_file:
        results = spec['ALGORITHM'].ranking_for_question (question_id,
                                                          spec['NB_OF_RESULTS'])
        json.dump(results, write_file)


def get_sample():
    sample = files.get_data (files.questions_sample)
    return sample


"""
For each scenario (A, B, C and D) runs the experiment
with the given specifications: paths to leave the results,
sample (described by number of participants), number of results.
"""


def main():
    global spec
    # Get sample of questions
    sample = get_sample ()

    # Start clicking
    start_time = datetime.datetime.now()

    # for scenario in SCENARIOS:
    for scenario in ['A']:
        spec['ALGORITHM'] = TMBAlgorithm (scenario)
        # Run experiment for each question in the sample
        for question_id in sample[:spec['SAMPLE_SIZE']]:
            now = print_header(question_id, scenario)

            filename = files.results_file (question_id, scenario, spec['NB_OF_PARTICIPANTS'])

            # Process and write results
            run_experiment(question_id, filename)

            print_footer(start_time, now)


if __name__ == '__main__':
    main()
