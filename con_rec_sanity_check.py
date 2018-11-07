#!/usr/bin/env python
# coding: utf-8

from con_rec import *
import json


def run_experiment(question_id, algorithm, nb_of_results):
    with open('data/results_for_' +
              str(question_id) +
              '.json', 'w') as write_file:
        results = w.ranking_for_question(question_id, nb_of_results)
        json.dump(results, write_file)


def main():
    import datetime
    import time
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
        sample_size = 100
        nb_of_results = 50
        start_time = datetime.datetime.now()
    for q in sample[:sample_size]:
        # Header
        print("------- start -------")
        print("question: " + str(q))
        now = datetime.datetime.now()
        print(now.strftime('%d-%m-%Y %H:%M:%S'))

        # Process and write results
        run_experiment_for(q, w, nb_of_results)

        # Footer
        print("\n" + str((datetime.datetime.now() - now).seconds) + " seconds")
        print(time.strftime('%H:%M:%S',
                            time.gmtime(str(
                                datetime.datetime.now() - start_time)
                                .seconds)) +
              " elapsed.")
        print("------- end -------\n\n")


if __name__ == '__main__':
    main()
