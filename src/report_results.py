#!/usr/bin/env python
# coding: utf-8

import csv
import src.utils.data_files as files
from src.utils.db import Database


SCENARIOS = ('A', 'B', 'C', 'D')


SAMPLE_SIZE = 100   # nb of questions in the sample
LIMIT_OF_RESULTS = 150  # size of the ranked users,
# defined in con_rec_sanity_check.py
BREAKS = list(range(5, LIMIT_OF_RESULTS + 5, 5))  # top5, top10, ..., top50
db = None
# Return the list of pairs (user,score) in order from higher to lower score


def full_ranking(question_id, scenario):
    data = files.get_data(files.results_file(question_id, scenario))
    return data


# Return the list of users in order from higher to lower score
def users_ranked(question_id, scenario):
    return list(map(lambda pair: pair[0], full_ranking(question_id, scenario)))


def ranking(question_id):
    users = users_ranked(question_id)
    ranking = {}
    for u in users:
        ranking[users.index(u)] = u
    return ranking


def participants_of_question(question_id):
    return list(map(lambda x: int(x),
                    db.participants_of_question(question_id)))

# Returns a list of percentage of participants in the top 5, 10, ... 50 results


def recall(question_id, scenario):
    users = users_ranked(question_id, scenario)

    participants = set(participants_of_question(question_id))

    nb_of_participants = len(participants)

    return list(map(lambda b: len(set(users[:b]) & participants) /
                    nb_of_participants,
                    BREAKS))


def main():
    global db
    sample = files.get_data(files.questions_sample)[:100]

    for scenario in SCENARIOS[0]:
        db = Database ()
        # Read results, get coverage and print it
        filename = files.results_dir(
            scenario) + '/results_scenario_' + scenario + '.csv'

        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')

            header = ['q_id'] + list(map(lambda b: 'top ' + str(b), BREAKS))
            writer.writerow(header)

            print('\t'.join(header))

            for question_id in sample:
                results = [question_id] + recall(question_id, scenario)
                users_ranked(question_id, scenario)
                print(participants_of_question(question_id))
                writer.writerow(results)

                print('\t'.join(map(str, results)))


if __name__ == '__main__':
    main()
