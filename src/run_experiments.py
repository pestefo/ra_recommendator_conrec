#!/usr/bin/env python
# coding: utf-8

'''
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm
from algorithms.tag_map_based_algorithm import TMBAlgorithm
from algorithms.closeness_to_asker_algorithm import C2AAlgorithm
'''
from algorithms.ranking_pseudokarma import RankingPseudoKarma
import json
import datetime
import time

dir_preffix = '/home/pestefo/projects/experiment_1/'
# path_to_results = 'data/tmba_100q_5p'
sample_file_path = dir_preffix + 'data/questions_with_5_participants.json'
# path_to_results = 'data/tmba_100q_1p'
# sample_file_path = 'data/questions_with_1_participant.json'
# path_to_results = 'data/wcfa_100q_5p_2nd_exp'
path_to_results = dir_preffix + 'data/rpk_100q_5p'
algorithm = RankingPseudoKarma()
default_sample_size = 100
default_nb_of_results = 150


def print_header(question_id):
    print("------- start -------")
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


def run_experiment(question_id, algorithm, nb_of_results):

    with open(path_to_results + '/results_for_' + str(question_id) + '.json',
              'w') as write_file:

        results = algorithm.ranking_for_question(question_id,
                                                 nb_of_results)
        json.dump(results, write_file)


def main():

    # Get sample of questions
    with open(sample_file_path, 'r') as sample_file:
        sample = json.load(sample_file)
        sample_size = default_sample_size
        nb_of_results = default_nb_of_results

    # Start clicking
    start_time = datetime.datetime.now()

    # Run experiment for each question in the sample
    for question_id in sample[:sample_size]:

        now = print_header(question_id)

        # Process and write results
        run_experiment(question_id, algorithm, nb_of_results)

        print_footer(start_time, now)


if __name__ == '__main__':
    main()
