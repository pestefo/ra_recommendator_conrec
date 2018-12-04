#!/usr/bin/env python
# coding: utf-8
from con_rec import AbstractConRecAlgorithm
from weighted_collaborative_filtering_algorithm import WCFAlgorithm
import json
from math import log
###
# Tag Map Based Algorithm (TMBA)
###


class TMBAlgorithm(AbstractConRecAlgorithm):

    user_tags = None
    question_tags = None
    tag_names = None
    r_ut_table = None
    r_ut_table_file = 'data/r_ut_2.json'
    nb_of_tags = None
    nb_of_questions = None
    wcfa = WCFAlgorithm()

    # Data files
    user_tags_file = 'data/ros_user_tag.json'
    question_tags_file = 'data/ros_question_tag.json'
    tags_file = 'data/ros_tag.json'

    def __init__(self):
        AbstractConRecAlgorithm.__init__(self)
        with open(TMBAlgorithm.r_ut_table_file) as json_data:
            TMBAlgorithm.r_ut_table = json.load(json_data)
            print("r_ut_table DONE")

        with open(TMBAlgorithm.user_tags_file) as json_data:
            TMBAlgorithm.user_tags = json.load(json_data)
            print("user_tags DONE")

        with open(TMBAlgorithm.question_tags_file) as json_data:
            TMBAlgorithm.question_tags = json.load(json_data)
            TMBAlgorithm.nb_of_questions = len(
                TMBAlgorithm.question_tags.keys())
            print("question_tags DONE")

        with open(TMBAlgorithm.tags_file) as json_data:
            TMBAlgorithm.tag_names = json.load(json_data)
            TMBAlgorithm.nb_of_tags = len(list(map(lambda pair: pair[0],
                                                   TMBAlgorithm.tag_names)))
            print("tag_names DONE")

    def all_users(self):
        return list(map(lambda k: int(k),
                        TMBAlgorithm.user_tags.keys()))

    def tags_of_user(self, user_id):
        return list(map(lambda pair: pair['tag'],
                        TMBAlgorithm.user_tags[str(user_id)]))

    def tags_of_question(self, question_id):
        return TMBAlgorithm.question_tags[str(question_id)]

    def valid_questions(self, questions):
        all_questions = self.all_questions
        return list(set(all_questions) & set(questions))

    def all_questions(self):
        return list(map(lambda q: int(q),
                        TMBAlgorithm.question_tags.keys()))

    def questions_with_tag(self, tag_id):
        questions = list(map(lambda q: int(q),
                             filter(lambda q: str(tag_id) in
                                    self.tags_of_question(q),
                                    self.all_questions())))
        return questions
        # return self.valid_questions(questions)

    def nb_of_tags(self):
        return TMBAlgorithm.nb_of_tags

    def nb_of_tags_of_question(self, question_id):
        return len(self.tags_of_question(question_id))

    def nb_of_questions(self):
        return TMBAlgorithm.nb_of_questions

    def calculate_r_ut(self, user_id, tag_id):
        questions = self.questions_with_tag(tag_id)

        # TODO: In theory, this should never happen
        if len(questions) == 0:
            return 0

        log_of_ratio = log(self.nb_of_questions / len(questions))
        return log_of_ratio * sum(map(lambda q: self.r_uq(user_id, q),
                                      questions))

    def r_ut(self, user_id, tag_id):
        try:
            return TMBAlgorithm.r_ut_table[str(user_id)][str(tag_id)]

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
