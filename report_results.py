#!/usr/bin/env python
# coding: utf-8

from con_rec import *
import json
import csv

t = TBMAAlgorithm()
w = TBMAAlgorithm.wcfa


def ranking_of_participants(question_id):
    participants = w.participants_of_question(question_id)
    with open('data/results_for_' + str(question_id) + '.json', 'r') as results_file:
        results = json.load(results_file)
        rank = list(map(lambda r: r[0], results))
    rank_of_participants = {}
    for u in participants:
        # ranking -> user_id
        rank_of_participants[rank.index(u)] = u
    return rank_of_participants


def percentage_of_coverage(question_id):
    rank = ranking_of_participants(question_id)
    nb_of_participants = len(rank.keys())
    stops = {5, 10, 15, 20, 25, 30, 35, 40, 45, 50}
    return list(map(lambda stop:
                    len(list(filter(lambda r:
                                    r <= stop,
                                    rank.keys()
                                    )
                             )
                        ) / nb_of_participants,
                    stops))


def main():
    import datetime

    # results = conrec.ranking_for_question(9061)
    # print(results)
    # tag = 49
    # u = 3
    # qs = t.questions_with_tag(tag)
    # print(sum(list(map(lambda q: t.wcfa.r_uq(u,q), qs))))

    with open('data/questions_with_5_participants.json', 'r') as sample_file:
        sample = json.load(sample_file)
        question_stop = 9686
        # print(percentage_of_coverage(9041))
    with open('data/perliminary_results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        header = ['top_5', 'top_10', 'top_15', 'top_20', 'top_25',
                  'top_30', 'top_35', 'top_40', 'top_45', 'top_50']
        print('\t'.join(header))
        writer.writerow(header)

        for q in sample[:52]:
            results = percentage_of_coverage(q)
            print("q = " + str(q))
            print('\t'.join(list(map(lambda s: str(s), results))))
            print("")
            writer.writerow(results)
            # with open('data/results_for_' + str(q) + '.json', 'w') as write_file:
            # results = w.ranking_for_question(q, nb_of_results)


if __name__ == '__main__':
    main()
