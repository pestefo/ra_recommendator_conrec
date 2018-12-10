#!/usr/bin/env python
# coding: utf-8
import csv


class RankingKarma():

    dir_preffix = '/home/pestefo/projects/experiment_1/'
    ranking_file = dir_preffix + 'data/ranking_karma.csv'
    ranking = None

    def __init__(self):
        RankingKarma.ranking = []

        with open(RankingKarma.ranking_file) as csv_data:
            reader = csv.reader(csv_data)
            reader.__next__()   # skip header
            
            # id,name,up_votes,down_votes,karma
            for row in reader:
                # id , pseudokarma
                RankingKarma.ranking.append((int(row[0]), int(row[-1])))

        max_value = RankingKarma.ranking[0][1]
        RankingKarma.ranking = list(map(
            lambda p: (p[0], p[1] / max_value),
            RankingKarma.ranking))

    def ranking_for_question(self, question, limit_of_results=150):
        if limit_of_results > 150:
            limit_of_results = 150

        return RankingKarma.ranking[:limit_of_results]
