#!/usr/bin/env python
# coding: utf-8
from operator import itemgetter
import json

'''
NOTES:
Be careful because some WCFAlgorithm's functions return dataframes as output
and TMBAlgorithm's return list of strings!!!

THERE ARE TAGS THAT ARE ONLY REFERRED IN USERS BUT NOT IN QUESTIONS
'''


class AbstractConRecAlgorithm:

    r_uq_table = None
    r_uq_table_file = './data/r_uq_2.json'
    all_questions = None

    def __init__(self):
        # Importing R_uq table
        # r_uq.csv to JSON from: http://www.convertcsv.com/csv-to-json.htm
        with open(AbstractConRecAlgorithm.r_uq_table_file) as json_data:
            AbstractConRecAlgorithm.r_uq_table = json.load(json_data)
            print("r_uq_table DONE")
        AbstractConRecAlgorithm.all_questions = list(
            map(lambda q: int(q),
                AbstractConRecAlgorithm.r_uq_table.keys()))
        print("all_questions DONE")

    # R_uq - Relation between a user and a question
    def r_uq(self, user_id, question_id):
        # val = r_uq_table[(r_uq_table['u'] ==
        #                   user_id) & (r_uq_table['q'] == question)]['r']
        try:
            return AbstractConRecAlgorithm.r_uq_table[
                str(question_id)][
                str(user_id)]

        except KeyError:
            # WE SUPPOSE THAT user_id and question_id are valid ids
            return 0

    def all_questions(self):
        return AbstractConRecAlgorithm.all_questions

    # Ranking
    # Top 15 candidates over 300 users
    def ranking_for_question(self, question, limit_of_results=150):
        results = map(lambda u: self.score(
            u, question), self.all_users())

        return sorted(results,
                      key=itemgetter(1),
                      reverse=True)[:limit_of_results]
