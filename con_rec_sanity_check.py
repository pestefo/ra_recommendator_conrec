#!/usr/bin/env python
# coding: utf-8

from con_rec import *
import json
import datetime
import time

# path_to_results = 'data/tmba_100q_5p'
# sample_file_path = 'data/questions_with_5_participants.json'
path_to_results = 'data/tmba_100q_1p'
sample_file_path = 'data/questions_with_1_participant.json'


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
    # Algorithms
    tmba = TMBAlgorithm()
    # wcfa = tmba.wcfa

    # Get sample of questions
    with open(sample_file_path, 'r') as sample_file:
        sample = json.load(sample_file)
        sample_size = 100
        nb_of_results = 150

    # Start clicking
    start_time = datetime.datetime.now()

    # Run experiment for each question in the sample
    for question_id in sample[:sample_size]:

        now = print_header(question_id)

        # Process and write results
        run_experiment(question_id, tmba, nb_of_results)

        print_footer(start_time, now)


if __name__ == '__main__':
    main()
