#!/usr/bin/env python
# coding: utf-8
from math import log

import src.algorithms.con_rec
from src.algorithms.scenarios import *


###
# Tag Map Based Algorithm (TMBA)
###


class TMBAlgorithm(src.algorithms.con_rec.AbstractConRecAlgorithm):

    def __init__(self, scenario: Scenario):

        src.algorithms.con_rec.AbstractConRecAlgorithm.__init__(self)

        self.scenario = scenario
        self.db = Database()
        self.user_tags = scenario.user_tag_container()
        self.question_tags = scenario.question_tag_container()
        self.R_UT_TABLE = files.get_data(self.scenario.r_ut_table())

    def r_ut_table(self):
        """

        :return: table of user_id,tag_id,r_ut
        :rtype: dict[str,dict[str,int]]
        """
        return self.R_UT_TABLE

    def all_users(self):
        """

        :return: a list of all users in the database
        :rtype: list[int]
        """
        return self.db.all_users()

    def all_questions(self):
        """

        :return: a list of all questions in the database
        :rtype: list[int]
        """
        return self.db.all_questions()

    def tags_of_user(self, user_id):
        """

        :param user_id: the id of a user
        :type user_id: int
        :return: a list with the tags associated to the user
        :rtype: list[int]
        """
        return self.user_tags.tag_ids_for(user_id)

    def tags_of_question(self, question_id):
        """

        :param question_id: the id of a question
        :type question_id: int
        :return: a list with the tags associated to the question
        :rtype: list[int]
        """
        return self.question_tags.tag_ids_for(question_id)

    def questions_with_tag(self, tag_id):
        """

        :param tag_id: the id of a tag
        :type tag_id: int
        :return: a list of questions that are described by certain tag
        :rtype: list[int]
        """
        return self.question_tags.questions_with_tag(tag_id)

    def nb_of_tags(self):
        """

        :return: number of tags in the database
        :rtype: int
        """
        return self.db.nb_of_tags

    def nb_of_tags_of_question(self, question_id):
        """

        :param question_id: the id of a question
        :type question_id: int
        :return: number of tags associated to certain question
        :rtype: int
        """
        return len(self.tags_of_question(question_id))

    def nb_of_questions(self):
        """

        :return: number of questions in the database
        :rtype: int
        """
        return self.db.nb_of_questions()

    def r_ut(self, user_id, tag_id):
        """

        :param user_id: the id of a user
        :type user_id: int
        :param tag_id: the id of a tag
        :type tag_id: int
        :return: the calculated number of R_ut for the user and tag provided
        :rtype: float
        """
        try:
            return self.r_ut_table()[str(user_id)][str(tag_id)]

        # If there's no calculated R_ut for that user_id and question_id
        # it means that user_id did not participate in question_id, then,
        # r_uq(user_id, question_id) = 0 => r_ut(user_id, question_id) = 0

        except KeyError:
            return 0

    def tags_in_common(self, user_id, question_id):
        """

        :param user_id: the id of a user
        :type user_id: int
        :param question_id: the id of a question
        :type question_id: int
        :return: the tags that have in common
        :rtype: set[int]
        """

        t_u = self.tags_of_user(user_id)
        t_q = self.tags_of_question(question_id)
        return set(t_u) & set(t_q)

    def score(self, user_id, question_id):
        """

        :param user_id: the id of a user
        :type user_id: int
        :param question_id: the id of a question
        :type question_id: int
        :return: the score of the user in that question using the Tag Map Based Algorithm
        :rtype: float
        """
        tags_in_common = self.tags_in_common(user_id, question_id)

        return user_id, len(tags_in_common) * sum(map(lambda t:
                                                      self.r_ut(user_id, t),
                                                      tags_in_common))

    def calculate_r_ut(self, user_id, tag_id):
        """

        :param user_id: the id of a user
        :type user_id: int
        :param tag_id: the id of a tag
        :type tag_id: int
        :return: the number of R_ut for that user and tag
        :rtype: float
        """
        questions = self.questions_with_tag(tag_id)

        if len(questions) == 0:
            return 0

        log_of_ratio = log(self.nb_of_questions() / len(questions))
        return log_of_ratio * sum(map(lambda q: self.r_uq(user_id, q),
                                      questions))
