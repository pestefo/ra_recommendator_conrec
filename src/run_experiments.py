#!/usr/bin/env python
# coding: utf-8

import json
import time

from tqdm import tqdm

from src.algorithms.experiment_samples import *
from src.algorithms.scenarios import *
from src.algorithms.tag_map_based_algorithm import TMBAlgorithm

# path_to_results = 'data/tmba_100q_5p'

# path_to_results = 'data/tmba_100q_1p'
# sample_file_path = 'data/questions_with_1_participant.json'
# path_to_results = 'data/wcfa_100q_5p_2nd_exp'

"""
Utils
"""


def run_experiment(question_id, algorithm, filename):
    """

    :param question_id: id of the question
    :type question_id: int
    :param algorithm: TMBAlgorithm instance
    :type algorithm: src.algorithms.con_rec.AbstractConRecAlgorithm
    :param filename: filename where to put the results
    :type filename: str
    :return: nothing
    :rtype: void
    """
    max_nb_of_results = 100

    with open(filename, 'w') as write_file:
        results = algorithm.ranking_for_question(question_id,
                                                 max_nb_of_results)
        json.dump(results, write_file)


"""
For each scenario (A, B, C and D) runs the experiment
with the given specifications: paths to leave the results,
sample (described by number of participants), number of results.
"""


def main():
    # Get sample of questions
    sample = Q100P5()
    date_and_time = time.strftime("%Y%m%d_%H%M")

    for scenario in Scenario.all_scenarios():
        algorithm = TMBAlgorithm(scenario)

        print("\n\n--- Starting {}---\n".format(scenario.name()))
        # Run experiment for each question in the sample
        for question_id in tqdm(sample.questions(), desc="question"):
            filename = files.path_to_results_of_question(date_and_time,
                                                         sample,
                                                         scenario,
                                                         question_id)

            # Process and write results
            run_experiment(question_id, algorithm, filename)


if __name__ == '__main__':
    main()
