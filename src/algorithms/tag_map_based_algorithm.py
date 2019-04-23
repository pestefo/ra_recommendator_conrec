#!/usr/bin/env python
# coding: utf-8
from algorithms.con_rec import AbstractConRecAlgorithm
from algorithms.weighted_collaborative_filtering_algorithm import WCFAlgorithm
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
    nb_of_tags = None
    nb_of_questions = None

    # Data files
    dir_preffix = '/home/pestefo/projects/ra_recommendator_conrec/'
    user_tags_file = dir_preffix + 'data/data_extracted_from_db/ros_user_tag.json'
    user_tags_extended_file = None
    r_ut_table_file = dir_preffix + 'data/r_ut.json'
    question_tags_file = dir_preffix + \
        'data/data_extracted_from_db/ros_question_tag.json'
    question_tags_extended_file = dir_preffix + \
        'data/ros_question_tag_extended.json'
    tags_file = dir_preffix + 'data/data_extracted_from_db/ros_tag.json'

    def __init__(self):
        AbstractConRecAlgorithm.__init__(self)
        TMBAlgorithm.r_ut_table = files.get_data(files.r_ut_table)
        TMBAlgorithm.user_tags = files.get_data(files.user_tags)
        TMBAlgorithm.question_tags_extended = files.get_data(
            files.question_tags_extended)
        TMBAlgorithm.nb_of_questions = len(
            TMBAlgorithm.question_tags.keys())

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
