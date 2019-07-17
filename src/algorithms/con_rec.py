#!/usr/bin/env python
# coding: utf-8
from operator import itemgetter
import src.utils.data_files as files
'''
NOTES:
Be careful because some WCFAlgorithm's functions return dataframes as output
and TMBAlgorithm's return list of strings!!!

THERE ARE TAGS THAT ARE ONLY REFERRED IN USERS BUT NOT IN QUESTIONS
'''


class AbstractConRecAlgorithm:

    # dir_preffix = '/home/pestefo/projects/experiment_1/'
    dir_preffix = '/home/pestefo/projects/ra_recommendator_conrec/'
    # r_uq_table_file = dir_preffix + 'data/r_uq_2.json'
    r_uq_table_file = dir_preffix + 'data/r_uq.json'
    r_uq_table = None
    all_questions = None

    def __init__(self):

        AbstractConRecAlgorithm.r_uq_table = files.get_data(files.r_uq_table)
        AbstractConRecAlgorithm.all_questions = list(
            map(lambda q: int(q),
                AbstractConRecAlgorithm.r_uq_table.keys()))

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
        """

        :param question: id of a question
        :type question: int
        :param limit_of_results: maximum amount of results to be returned
        :type limit_of_results:  int
        :return: a sorted list of pairs [user_id, score] from higher to lower score
        :rtype: list[list[int,float]]
        """
        results = map(lambda u: self.score(
            u, question), self.all_users())

        return sorted(results,
                      key=itemgetter(1),
                      reverse=True)[:limit_of_results]
