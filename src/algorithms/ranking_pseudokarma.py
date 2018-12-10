#!/usr/bin/env python
# coding: utf-8
import csv


class RankingPseudoKarma():

    dir_preffix = '/home/pestefo/projects/experiment_1/'
    ranking_file = dir_preffix + 'data/ranking_pseudokarma.csv'
    ranking = None

    def __init__(self):
        RankingPseudoKarma.ranking = []
        with open(RankingPseudoKarma.ranking_file) as csv_data:
            reader = csv.reader(csv_data)
            reader.__next__()   # skip header

            # author,resp_acc,id,name,up_votes,down_votes,pseudokarma
            for row in reader:
                # id , pseudokarma
                RankingPseudoKarma.ranking.append((int(row[0]), int(row[-1])))

        max_value = RankingPseudoKarma.ranking[0][1]
        RankingPseudoKarma.ranking = list(map(
            lambda p: (p[0], p[1] / max_value),
            RankingPseudoKarma.ranking))

    def ranking_for_question(self, question, limit_of_results=150):
        if limit_of_results > 150:
            limit_of_results = 150

        return RankingPseudoKarma.ranking[:limit_of_results]
