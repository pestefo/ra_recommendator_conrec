#!/usr/bin/env python
# coding: utf-8

import csv

from tqdm import tqdm

from src.algorithms.scenarios import *


def data_from_results_directory(s):
    return s[:13], int(s[-2:-1])


"""
IMPORTANT!!! Give the correct results_directory!
"""
results_directory = '20190717_1108_5p'

date_and_time, nb_of_participants = data_from_results_directory(results_directory)
db = Database()
limit_of_results = 150
breaks = list(range(5, limit_of_results + 5, 5))  # top5, top10, ..., top50


def users_ranked(path_to_results):
    """
    It gets a sorted list of tuples in JSON like this: [[user_id, score], ... ]
    and returns only the user_ids keeping the ranking order

    :param path_to_results: path to the file where results are stores
    :type path_to_results: str
    :return: a list of users and scores sorted by score
    :rtype: list[int]
    """

    return list(map(lambda pair: pair[0], files.get_data(path_to_results)))


def recall(question_id, ranking_of_users):
    """

    :param question_id: id of a question
    :type question_id: int
    :param ranking_of_users: list of users ranked desc by score
    :type ranking_of_users: list[int]
    :return: list of recalls per 5, 10, 15, ..., 100 participants in the ranking
    :rtype: list[float]
    """
    global db, limit_of_results, breaks, nb_of_participants

    def participants_of_question(q_id):
        return list(map(lambda x: int(x),
                        db.participants_of_question(q_id)))

    participants = set(participants_of_question(question_id))

    return list(map(lambda b:
                    len(set(ranking_of_users[:b]) & participants) / nb_of_participants,
                    breaks))


def main():
    global db, breaks, date_and_time, nb_of_participants

    print("\n\n--- Sample: {}_{}p---\n\n\n".format(date_and_time, nb_of_participants))

    for scenario in Scenario.all_scenarios():
        print("\n\n--- Starting {}---\n".format(scenario.name()))
        # Read results, get coverage and print it
        filename = files.filename_of_recall_of_scenario_and_nb_of_participants(date_and_time,
                                                                               scenario,
                                                                               nb_of_participants)

        with open(filename, 'w') as fp:
            writer = csv.writer(fp, delimiter='\t')

            # Write header
            header = ['q_id'] + list(map(lambda b: 'top ' + str(b), breaks))
            writer.writerow(header)

            # Dict: question_id -> path_to_question_id_results_json_file
            question_file_paths = files.question_result_files(date_and_time,
                                                              nb_of_participants,
                                                              scenario)

            for question_id, path_to_results in tqdm(question_file_paths.items()):
                ranking_of_users = users_ranked(path_to_results)

                # Write results
                results = [question_id] + recall(question_id, ranking_of_users)
                writer.writerow(results)


if __name__ == '__main__':
    main()
