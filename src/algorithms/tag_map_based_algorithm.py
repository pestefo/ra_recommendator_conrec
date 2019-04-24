#!/usr/bin/env python
# coding: utf-8
from algorithms.con_rec import AbstractConRecAlgorithm
import utils.data_files as files

###
# Tag Map Based Algorithm (TMBA)
###


class TMBAlgorithm(AbstractConRecAlgorithm):
    from utils.db import Database

    def __init__(self, scenario='B'):
        print("------ TMBA Scenario {} ------".format(scenario))

        AbstractConRecAlgorithm.__init__(self)

        self.r_ut_table = files.get_data(files.r_ut_table_scenario[scenario])

        self.tag_names = files.get_data(files.tags_file)
        self.nb_of_tags = len(list(map(lambda pair: pair[0], self.tag_names)))

    def all_users(self):
        return self.db.all_users()

    def all_questions(self):
        # return list(map(lambda q: int(q),
        #                 self.question_tags.keys()))
        return self.db.all_questions()

    def tags_of_user(self, user_id):
        # return list(map(lambda pair: pair['tag'],
        #                 self.user_tags[str(user_id)]))
        return self.db.tags_of_user(self.scenario, user_id)

    def tags_of_question(self, question_id):
        # return self.question_tags[str(question_id)]
        return self.db.tags_of_question(self.scenario, question_id)

    # def valid_questions(self, questions):
    #     all_questions=self.all_questions
    #     return list(set(all_questions) & set(questions))

    def questions_with_tag(self, tag_id):
        # questions=list(map(lambda q: int(q), filter(lambda q: str(
        #     tag_id) in self.tags_of_question(q), self.all_questions())))
        # return questions
        return self.db.questions_with_tag(self.scenario, tag_id)

    def nb_of_tags(self):
        return self.nb_of_tags

    def nb_of_tags_of_question(self, question_id):
        return len(self.tags_of_question(question_id))

    def nb_of_questions(self):
        return self.nb_of_questions

    def r_ut(self, user_id, tag_id):
        try:
            return self.r_ut_table[str(user_id)][str(tag_id)]

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
