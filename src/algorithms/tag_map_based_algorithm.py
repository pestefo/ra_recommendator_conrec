#!/usr/bin/env python
# coding: utf-8
from math import log

import src.algorithms.con_rec
from src.algorithms.scenarios import *


###
# Tag Map Based Algorithm (TMBA)
###


class TMBAlgorithm (src.algorithms.con_rec.AbstractConRecAlgorithm):

    def __init__(self, scenario: Scenario):

        src.algorithms.con_rec.AbstractConRecAlgorithm.__init__ (self)

        self.scenario = scenario
        self.db = Database ()
        self.user_tags = scenario.user_tag_container ()
        self.question_tags = scenario.question_tag_container ()

    def r_ut_table(self):
        if not self.R_UT_TABLE:
            self.R_UT_TABLE = files.get_data (self.scenario.r_ut_table ())

        return self.R_UT_TABLE

    def all_users(self):
        return self.db.all_users ()

    def all_questions(self):
        return self.db.all_questions ()

    def tags_of_user(self, user_id):
        return self.user_tags.tag_ids_for (user_id)

    def tags_of_question(self, question_id):
        return self.question_tags.tag_ids_for (question_id)

    def questions_with_tag(self, tag_id):
        return self.question_tags.questions_with_tag (tag_id)

    def nb_of_tags(self):
        return self.db.nb_of_tags

    def nb_of_tags_of_question(self, question_id):
        return len (self.tags_of_question (question_id))

    def nb_of_questions(self):
        return self.db.nb_of_questions ()

    def r_ut(self, user_id, tag_id):
        try:
            for pair in self.r_ut_table ()[str (user_id)]:

                if pair['t'] == int (tag_id):
                    return pair['r']

        # If there's no calculated R_ut for that user_id and question_id
        # it means that user_id did not participate in question_id, then,
        # r_uq(user_id, question_id) = 0 => r_ut(user_id, question_id) = 0

        except Exception:
            return 0

        return 0

    def tags_in_common(self, user_id, question_id):

        t_u = self.tags_of_user (user_id)
        t_q = self.tags_of_question (question_id)
        return set (t_u) & set (t_q)

    def score(self, user_id, question_id):
        tags_in_common = self.tags_in_common (user_id, question_id)
        # print('u:' + str(user_id) + '\tq:' + str(question_id) +
        #       '\ttags_common:' + str(tags_in_common))
        return user_id, len (tags_in_common) * \
               sum (map (lambda t:
                         self.r_ut (user_id, t),
                         tags_in_common))

    def calculate_r_ut(self, user_id, tag_id):
        questions = self.questions_with_tag (tag_id)

        if len (questions) == 0:
            return 0

        log_of_ratio = log (self.nb_of_questions () / len (questions))
        print (list (map (lambda q: self.r_uq (user_id, q), questions)))
        return log_of_ratio * sum (map (lambda q: self.r_uq (user_id, q),
                                        questions))
