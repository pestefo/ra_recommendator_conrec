#!/usr/bin/env python
# coding: utf-8
from random import randint
from operator import itemgetter


class MockRanking:
    ranking = None

    def __init__(self):
        MockRanking.ranking = []
        MAX_NUM_USERS = 43872
        MAX_SCORE = 2500
        for i in range(1,150):
            MockRanking.ranking.append((randint(1,MAX_NUM_USERS), randint(1,MAX_SCORE)))

        MockRanking.ranking = sorted(MockRanking.ranking, key=itemgetter(1),reverse=True)

    def ranking_for_question(self, question, limit_of_results=150):
        return MockRanking.ranking[:limit_of_results]