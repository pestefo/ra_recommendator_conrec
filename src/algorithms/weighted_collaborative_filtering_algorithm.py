#!/usr/bin/env python
# coding: utf-8

from algorithms.con_rec import AbstractConRecAlgorithm
import pandas as pd
from math import sqrt


class WCFAlgorithm(AbstractConRecAlgorithm):

    # dir_preffix = '/home/pestefo/projects/experiment_1/'
    dir_preffix = '/home/pestefo/projects/ra_recommendator_conrec/'
    act_ans_comm = None
    act_ask = None
    total_activities = None

    db_file = dir_preffix + 'data/v1.2.db'

    def __init__(self):
        AbstractConRecAlgorithm.__init__(self)
        self.extract_data_from_db()

    def extract_data_from_db(self):
        import sqlite3
        conn = sqlite3.connect(WCFAlgorithm.db_file)

        # Activity: asking and commenting a question
        query_activity_ans_comm = """
        select active_users.q_id, active_users.u_id as u_id , count(*) as activity
        from
        (
            select rqa.ros_question_id as q_id, ra.author as u_id
            from ros_question_answer as rqa
            left join ros_answer as ra on rqa.ros_answer_id = ra.id
        ) as active_users
        group by q_id, u_id
        """

        # Activity: asking a question
        query_activity_ask = """
        select q_id, author as u_id, 1 as activity
        from
        (
            select distinct ros_question_answer.ros_question_id as q_id
            from ros_question_answer
        ) as questions
        left join ros_question as rq on questions.q_id = rq.id
        """

        # Total nb of activities per question
        query_total_activities = """
        select ros_question_id, count(*)+1 as total_activities
        from ros_question_answer
        group by ros_question_id
        """

        # Running queries
        WCFAlgorithm.act_ask = pd.read_sql_query(query_activity_ask, conn)
        print("act_ask DONE")

        WCFAlgorithm.act_ans_comm = pd.read_sql_query(
            query_activity_ans_comm, conn)
        print("act_ans_comm DONE")

        WCFAlgorithm.total_activities = pd.read_sql_query(
            query_total_activities, conn)
        print("total_activities DONE")

        conn.close()

    def activity_ans_comm(self, user_id, question_id):
        val = WCFAlgorithm.act_ans_comm[
            (WCFAlgorithm.act_ans_comm['u_id'] == user_id) &
            (WCFAlgorithm.act_ans_comm['q_id'] == question_id)
        ]["activity"]

        if val.empty:
            return 0
        return val.values[0]

    def activity_ask(self, user_id, question_id):
        val = WCFAlgorithm.act_ask[
            (WCFAlgorithm.act_ask['u_id'] == user_id) &
            (WCFAlgorithm.act_ask['q_id'] == question_id)
        ]["activity"]
        if val.empty:
            return 0
        return val.values[0]

    def question_activities(self, question_id):
        return WCFAlgorithm.total_activities[
            WCFAlgorithm.total_activities['ros_question_id'] ==
            question_id
        ]["total_activities"].values[0]

    def all_users(self,):
        return pd.concat([WCFAlgorithm.act_ans_comm['u_id'],
                          WCFAlgorithm.act_ask['u_id']]).drop_duplicates()

    # Activity

    def activity(self, user_id, question_id):
        return self.activity_ans_comm(user_id, question_id) + \
            self.activity_ask(user_id, question_id)

    # List of participants in a question - U_{q}

    def participants_of_question(self, question_id):
        return list(map(lambda u: int(u),
                        WCFAlgorithm.r_uq_table[str(question_id)].keys()))

    def participants_of_question2(self, question_id):
        answerers = WCFAlgorithm.act_ans_comm[
            (WCFAlgorithm.act_ans_comm['q_id'] == question_id) &
            (WCFAlgorithm.act_ans_comm['activity'] > 0)
        ]["u_id"]

        askers = WCFAlgorithm.act_ask[
            (WCFAlgorithm.act_ask['q_id'] == question_id) &
            (WCFAlgorithm.act_ask['activity'] > 0)
        ]["u_id"]

        return pd.concat([answerers, askers]).drop_duplicates()

    def questions_for_user(self, user):
        questions_answered = WCFAlgorithm.act_ans_comm[
            (WCFAlgorithm.act_ans_comm['u_id'] == user) &
            (WCFAlgorithm.act_ans_comm['activity'] > 0)
        ]["q_id"]

        questions_asked = WCFAlgorithm.act_ask[
            (WCFAlgorithm.act_ask['u_id'] == user) &
            (WCFAlgorithm.act_ask['activity'] > 0)
        ]["q_id"]

        return set(pd.concat([questions_answered,
                              questions_asked]).drop_duplicates())

    def questions_in_common(self, users):
        questions = self.questions_for_user(users[0])
        for user in users[1:]:
            questions &= self.questions_for_user(user)
            if not questions:
                return set()
        return questions

    # Old implementation for calculating r_uq
    def calculate_r_uq(self, user, question):
        if self.activity(user, question) == 0:
            return 0
        return self.activity(user, question) / \
            self.question_activities(question)

    # R_uu - Relation between two users
    def r_uu(self, user_a, user_b):
        q_in_common = self.questions_in_common([user_a, user_b])
        q_a = self.questions_for_user(user_a)
        q_b = self.questions_for_user(user_b)
        a = sum(map(lambda q: self.r_uq(user_a, q) * self.r_uq(user_b, q),
                    q_in_common))
        b = sqrt(sum(map(lambda q: self.r_uq(user_a, q)**2,
                         q_a)) *
                 sum(map(lambda q: self.r_uq(user_b, q)**2,
                         q_b)))
        if a == 0:
            return 0
        return a / b

    # Score of a user to be a suitable for a question
    def score(self, candidate, question):
        return candidate, sum(map(lambda u: self.r_uq(u, question) *
                                  self.r_uu(candidate, u),
                                  self.participants_of_question(question)))
