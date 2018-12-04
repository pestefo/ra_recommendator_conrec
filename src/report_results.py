#!/usr/bin/env python
# coding: utf-8

from algorithms.weighted_collaborative_filtering_algorithm import *
import json
import csv


# t = TMBAlgorithm()
w = WCFAlgorithm()
# path_to_results = 'data/wcfa_100q_5p/'
# report_filename = 'results_wcfa_100q_5p.csv'
# path_to_results = 'data/tmba_100q_5p/'
# report_filename = 'results_tmba_100q_5p.csv'
dir_preffix = '/home/pestefo/projects/experiment_1/'
path_to_results = dir_preffix + 'data/rpk_100q_5p/'
sample_file_path = dir_preffix + 'data/questions_with_5_participants.json'
report_filename = 'results_wcfa_100q_5p_2nd_exp.csv'
# sample_file_path = 'data/questions_with_1_participant.json'
# nb of questions in the sample
sample_size = 100

# size of the ranked users, defined in con_rec_sanity_check.py
limit_of_results = 150
breaks = list(range(5, limit_of_results + 5, 5))  # top5, top10, ..., top50

# Return the list of pairs (user,score) in order from higher to lower score


def full_ranking(question_id):
    path_to_result_file = path_to_results + \
        'results_for_' + str(question_id) + '.json'
    with open(path_to_result_file, 'r') as results_file:
        return json.load(results_file)


# Return the list of users in order from higher to lower score
def users_ranked(question_id):
    return list(map(lambda pair: pair[0], full_ranking(question_id)))


def ranking(question_id):
    users = users_ranked(question_id)
    ranking = {}
    for u in users:
        ranking[users.index(u)] = u
    return ranking

# Returns a list of percentage of participants in the top 5, 10, ... 50 results


def recall(question_id):
    users = users_ranked(question_id)
    participants = set(w.participants_of_question(question_id))
    nb_of_participants = len(participants)

    return list(map(lambda b: len(set(users[:b]) & participants) /
                    nb_of_participants,
                    breaks))


def main():

    with open(sample_file_path, 'r') as sample_file:
        sample = json.load(sample_file)[:sample_size]

    # Read results, get coverage and print it
    with open(path_to_results + report_filename, 'w'
              ) as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        header = ['q_id'] + list(map(lambda b: 'top ' + str(b), breaks))
        writer.writerow(header)
        print('\t'.join(header))

        for question_id in sample:
            results = [question_id] + recall(question_id)
            writer.writerow(results)
            print('\t'.join(map(str, results)))


if __name__ == '__main__':
    main()
