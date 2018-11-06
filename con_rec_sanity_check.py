#!/usr/bin/env python
# coding: utf-8

from con_rec import *
import json


def main():
    import datetime
    t = TBMAAlgorithm()
    w = TBMAAlgorithm.wcfa
    # results = conrec.ranking_for_question(9061)
    # print(results)
    # tag = 49
    # u = 3
    # qs = t.questions_with_tag(tag)
    # print(sum(list(map(lambda q: t.wcfa.r_uq(u,q), qs))))

    with open('data/questions_with_5_participants.json', 'r') as sample_file:
        sample = json.load(sample_file)
        runs = 100
        nb_of_results = 50
        start_time = datetime.datetime.now()
    for q in sample[:runs]:
        print("------- start -------")
        print("question: " + str(q))
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        with open('data/results_for_' + str(q) + '.json', 'w') as write_file:
            results = w.ranking_for_question(q, nb_of_results)
            json.dump(results, write_file)
        print("\n" + str((datetime.datetime.now() - now).seconds) + " seconds")
        print(str((datetime.datetime.now() - start_time).seconds) +
              " seconds elapsed.")
        print("------- end -------\n\n")


if __name__ == '__main__':
    main()
