#!/usr/bin/env python
# coding: utf-8

'''
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm
from algorithms.tag_map_based_algorithm import TMBAlgorithm
from algorithms.closeness_to_asker_algorithm import C2AAlgorithm
'''
from algorithms.tag_map_based_algorithm import TMBAlgorithm
from utils import data_files as files
import json
import datetime
import time

# path_to_results = 'data/tmba_100q_5p'

# path_to_results = 'data/tmba_100q_1p'
# sample_file_path = 'data/questions_with_1_participant.json'
# path_to_results = 'data/wcfa_100q_5p_2nd_exp'

ALGORITHM = None
SAMPLE_SIZE = 100
NB_OF_RESULTS = 150
SCENARIOS = ('A', 'B', 'C', 'D')


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
                            datetime.datetime.now() - start_time)
                            .seconds)) +
          " elapsed.")
    print("------- end -------\n\n")


def run_experiment(question_id, filename):
    global NB_OF_RESULTS, ALGORITHM
    with open(filename, 'w') as write_file:

        results = ALGORITHM.ranking_for_question(question_id,
                                                 NB_OF_RESULTS)
        json.dump(results, write_file)


def main():
    global SAMPLE_SIZE, SCENARIOS, ALGORITHM
    # Get sample of questions
    sample = files.get_data(files.questions_sample)

    # Start clicking
    start_time = datetime.datetime.now()

    # for scenario in SCENARIOS:
    for scenario in ['A']:
        ALGORITHM = TMBAlgorithm(scenario)
        # Run experiment for each question in the sample
        for question_id in sample[:SAMPLE_SIZE]:
            now = print_header(question_id, scenario)

            filename = files.results_file(question_id, scenario)

            # Process and write results
            run_experiment(question_id, filename)

            print_footer(start_time, now)


if __name__ == '__main__':
    main()
