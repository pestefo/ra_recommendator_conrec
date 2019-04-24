#!/usr/bin/env python
# coding: utf-8
from algorithms.con_rec import AbstractConRecAlgorithm
import utils.data_files as files
from utils.db import Database
###
# Tag Map Based Algorithm (TMBA)
###


class TMBAlgorithm(AbstractConRecAlgorithm):

    def __init__(self, scenario='B'):
        print("------ TMBA Scenario {} ------".format(scenario))

        AbstractConRecAlgorithm.__init__(self)

        self.R_UT_TABLE = files.get_data(files.r_ut_table_scenario[scenario])
        self.db = Database(scenario)

    def all_users(self):
        return self.db.all_users()

    def all_questions(self):
        return self.db.all_questions()

    def tags_of_user(self, user_id):
        return self.db.tags_of_user(self.scenario, user_id)

    def tags_of_question(self, question_id):
        return self.db.tags_of_question(self.scenario, question_id)

    def questions_with_tag(self, tag_id):
        return self.db.questions_with_tag(self.scenario, tag_id)

    def nb_of_tags(self):
        return self.db.nb_of_tags()

    def nb_of_tags_of_question(self, question_id):
        return len(self.tags_of_question(question_id))

    def nb_of_questions(self):
        return self.db.nb_of_questions()

    def r_ut(self, user_id, tag_id):
        try:
            return self.R_UT_TABLE[str(user_id)][str(tag_id)]

        except KeyError:
            # WE SUPPOSE THAT user_id and question_id are valid ids
            return 0

    def tags_in_common(self, user_id, question_id):

        t_u = self.tags_of_user(user_id)
        t_q = self.tags_of_question(question_id)
        return set(t_u) & set(t_q)

    def score(self, user_id, question_id):
        tags_in_common = self.tags_in_common(user_id, question_id)
        # print('u:' + str(user_id) + '\tq:' + str(question_id) +
        #       '\ttags_common:' + str(tags_in_common))
        return user_id, len(tags_in_common) * \
            sum(map(lambda t:
                    self.r_ut(user_id, t),
                    tags_in_common))
