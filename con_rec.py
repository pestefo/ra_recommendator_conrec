#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from math import sqrt, log
from operator import itemgetter, attrgetter
import json

'''
NOTES:
Be careful because some WCFAlgorithm's functions return dataframes as output
and TBMAAlgorithm's return list of strings!!!

THERE ARE TAGS THAT ARE ONLY REFERRED IN USERS BUT NOT IN QUESTIONS
'''


class WCFAlgorithm:

    act_ans_comm = None
    act_ask = None
    total_activities = None
    all_questions = None
    r_uq_table = None
    r_uq_table_file = './data/r_uq_2.json'
    db_file = 'v1.db'

    def __init__(self):
        self.extract_data_from_db()
        # Importing R_uq table
        # r_uq.csv to JSON from: http://www.convertcsv.com/csv-to-json.htm
        with open(WCFAlgorithm.r_uq_table_file) as json_data:
            WCFAlgorithm.r_uq_table = json.load(json_data)
            print("r_uq_table DONE")
        WCFAlgorithm.all_questions = list(map(lambda q: int(q),
                                              WCFAlgorithm.r_uq_table.keys()))
        print("all_questions DONE")

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
        val = WCFAlgorithm.act_ans_comm[(WCFAlgorithm.act_ans_comm['u_id'] == user_id) & (
            WCFAlgorithm.act_ans_comm['q_id'] == question_id)]["activity"]
        if val.empty:
            return 0
        return val.values[0]

    def activity_ask(self, user_id, question_id):
        val = WCFAlgorithm.act_ask[(WCFAlgorithm.act_ask['u_id'] == user_id) & (
            WCFAlgorithm.act_ask['q_id'] == question_id)]["activity"]
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

    def all_questions(self,):
        return pd.concat([WCFAlgorithm.act_ans_comm['u_id'],
                          WCFAlgorithm.act_ask['u_id']]).drop_duplicates()

    # Activity

    def activity(self, user_id, question_id):
        return self.activity_ans_comm(user_id, question_id) + self.activity_ask(user_id, question_id)

    # List of participants in a question - U_{q}

    def participants_of_question(self, question_id):
        return list(map(lambda u: int(u),
                        WCFAlgorithm.r_uq_table[str(question_id)].keys()))

    def participants_of_question2(self, question_id):
        answerers = WCFAlgorithm.act_ans_comm[
            (WCFAlgorithm.act_ans_comm['q_id'] == question_id) &
            (WCFAlgorithm.act_ans_comm['activity'] > 0)
        ]["u_id"]
        askers = WCFAlgorithm.act_ask[(WCFAlgorithm.act_ask['q_id'] == question_id) &
                                      (WCFAlgorithm.act_ask['activity'] > 0)]["u_id"]
        return pd.concat([answerers, askers]).drop_duplicates()

    def questions_for_user(self, user):
        questions_answered = WCFAlgorithm.act_ans_comm[
            (WCFAlgorithm.act_ans_comm['u_id'] == user) &
            (WCFAlgorithm.act_ans_comm['activity'] > 0)
        ]["q_id"]
        questions_asked = WCFAlgorithm.act_ask[(WCFAlgorithm.act_ask['u_id'] == user) & (
            WCFAlgorithm.act_ask['activity'] > 0)]["q_id"]
        return set(pd.concat([questions_answered,
                              questions_asked]).drop_duplicates())

    def questions_in_common(self, users):
        questions = self.questions_for_user(users[0])
        for user in users[1:]:
            questions &= self.questions_for_user(user)
            if not questions:
                return set()
        return questions

    # R_uq - Relation between a user and a question
    def r_uq(self, user_id, question_id):
        # val = r_uq_table[(r_uq_table['u'] ==
        #                   user_id) & (r_uq_table['q'] == question)]['r']
        try:
            return WCFAlgorithm.r_uq_table[str(question_id)][str(user_id)]

        except KeyError:
            # WE SUPPOSE THAT user_id and question_id are valid ids
            return 0

    # Old implementation for calculating r_uq

    def calculate_r_uq(self, user, question):
        if self.activity(user, question) == 0:
            return 0
        return self.activity(user, question) / self.question_activities(question)

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
    def result(self, user, question):
        return user, sum(map(lambda u: self.r_uq(u, question) *
                             self.r_uu(user, u),
                             self.participants_of_question(question)))

    # Ranking
    # Top 15 candidates over 300 users
    def ranking_for_question(self, question, limit):
        # if limit = 50  # let's work with 15 the top results only
        # nb_of_users = 300
        results = map(lambda u: self.result(
            u, question), self.all_users())
        return sorted(results, key=itemgetter(1), reverse=True)[:limit]


'''
    def example(self):

        # Tests for activity_ans_comm
        # print("\nTests: activity_ans_comm")
        # print("-----")
        # print(activity_ans_comm(0,9045) == 0)
        # print(activity_ans_comm(3,9045) == 1)
        # print(activity_ans_comm(23668,9045) == 2)
            # Tests for activity_task
        # print("\nTests: activity_task")
        # print("-----")
        # print("activity_ask(7,9045) == 1\t"+str(activity_ask(7,9045) == 1)) # True
        # print("activity_ask(3,9045) == 0\t"+str(activity_ask(3,9045) == 0)) # True
        # print("activity_ask(23668,9045) == 0\t"+str(activity_ask(23668,9045) == 0)) # True
            # Tests for question_activities
        # print("\nTests: question_activities")
        # print("-----")
        # print("question_activities(9033) == 4\t\t"+str(question_activities(9033) == 4)) # True
        # print("question_activities(9190) == 14\t\t"+str(question_activities(9190) == 14)) # True
        # print("question_activities(236154) == 9\t"+str(question_activities(236154) == 9)) # True
            # print("Question ID: 9045")
        # print("-----------------")
        # print("Asker ID = 7, Answers/Commenters = 3, 5184, 23668")
        # print(participants_of_question(9045))

        # List of questions in which a user participates - Q_{u}

            # print("")
        # print("# Questions for user 7\t\t: "+str(len(questions_for_user(7)))) # participated: 2520,
        # print("# Questions for user 3\t\t: "+str(len(questions_for_user(3))))
        # print("# Questions for user 5184\t: "+str(len(questions_for_user(5184))))
        # print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(set(questions_for_user(23668)) & set(questions_for_user(5184)) & set(questions_for_user(3)) & set(questions_for_user(7))))
        # print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(questions_in_common([3, 5184, 23668, 7])))
        # print("Users 3, and 7 --> "+str(questions_in_common([3, 7])))
            # print(" ")
        print("Relation user-question (r_uq)")
        print("Asker\t\t:\tr_uq(7,9045)= " + str(self.r_uq(7, 9045)))
        print("Answerer\t:\tr_uq(3,9045)= " + str(self.r_uq(3, 9045)) +
              " (provides the accepted answer)")
        print("Participant\t:\tr_uq(5184,9045)= " +
              str(self.r_uq(5184, 9045)) + " (participated twice)")
        # print(" ")
        print("Relation user-user (r_uu)")
        print("Asker-Answerer\t\t:\tr_uu(7,3)= " + str(self.r_uu(7, 3)))
        print("Asker-Participant\t:\tr_uu(7,5184)= " + str(self.r_uu(7, 5184)))
        print("Answerer-Participant\t:\tr_uu(3,5184)= " +
              str(self.r_uu(5184, 3)))

        # -----
        show_tests = True

        if show_tests:
            print(" ")
            print("Results for Q_id=9045")
            print("Asker\t\t:\tresult(7,9045)= " + str(self.result(7, 9045)))
            print("Answerer\t:\tresult(3,9045)= " +
                  str(self.result(3, 9045)) +
                  " (provides the accepted answer)")
            print("Participant\t:\tresult(5184,9045)= " +
                  str(self.result(5184, 9045)) + " (participated twice)")

            # -----
        show_ranking = True

        if show_ranking:
            print(" ")
            print("Ranking for q=9045")
            print("------------------")
            ranking = self.ranking_for_question(9045)
            print(str(ranking))
            for result in ranking:
                print(str(result[0]) + " - " + str(result[1]))
'''


class TBMAAlgorithm:

    user_tags = None
    question_tags = None
    tag_names = None
    r_ut_table = None
    nb_of_tags = None
    nb_of_questions = None
    wcfa = WCFAlgorithm()

    # Data files
    user_tags_file = 'data/ros_user_tag.json'
    question_tags_file = 'data/ros_question_tag.json'
    tags_file = 'data/ros_tag.json'

    def __init__(self):

        with open(TBMAAlgorithm.user_tags_file) as json_data:
            TBMAAlgorithm.user_tags = json.load(json_data)
            print("user_tags DONE")

        with open(TBMAAlgorithm.question_tags_file) as json_data:
            TBMAAlgorithm.question_tags = json.load(json_data)
            TBMAAlgorithm.nb_of_questions = len(
                TBMAAlgorithm.question_tags.keys())
            print("question_tags DONE")

        with open(TBMAAlgorithm.tags_file) as json_data:
            TBMAAlgorithm.tag_names = json.load(json_data)
            TBMAAlgorithm.nb_of_tags = len(list(map(lambda pair: pair[0],
                                                    TBMAAlgorithm.tag_names)))
            print("tag_names DONE")

    def all_users(self):
        return list(map(lambda k: int(k),
                        TBMAAlgorithm.user_tags.keys()))

    def tags_of_user(self, user_id):
        return list(map(lambda pair: pair['tag'],
                        TBMAAlgorithm.user_tags[str(user_id)]))

    def tags_of_question(self, question_id):
        return TBMAAlgorithm.question_tags[str(question_id)]

    def valid_questions(self, questions):
        all_questions = TBMAAlgorithm.wcfa.all_questions
        return list(set(all_questions) & set(questions))

    def all_questions(self):
        return list(map(lambda q: int(q),
                        TBMAAlgorithm.question_tags.keys()))

    def questions_with_tag(self, tag_id):
        questions = list(map(lambda q: int(q),
                             filter(lambda q: str(tag_id) in
                                    self.tags_of_question(q),
                                    self.all_questions())))
        return questions
        # return self.valid_questions(questions)

    def nb_of_tags(self):
        return TBMAAlgorithm.nb_of_tags

    def nb_of_tags_of_question(self, question_id):
        return len(self.tags_of_question(question_id))

    def calculate_r_ut(self, user_id, tag_id):
        w = TBMAAlgorithm.wcfa
        questions = self.questions_with_tag(tag_id)

        # TODO: In theory, this should never happen
        if len(questions) == 0:
            return 0

        log_of_ratio = log(TBMAAlgorithm.nb_of_questions / len(questions))
        return log_of_ratio * sum(map(lambda q: w.r_uq(user_id, q),
                                      questions))

    def r_ut(self, user_id, tag):
        pass

    def tags_in_common(self, user_id, question_id):
        t_u = self.tags_of_user(user_id)
        t_q = self.tags_of_question(question_id)
        return set(t_u) & set(t_q)

    def result(self, user_id, question_id):
        tags_in_common = self.tags_in_common(user_id, question_id)
        return user_id, len(tags_in_common) * sum(map(lambda t:
                                                      self.r_ut(user_id, t),
                                                      tags_in_common))

    # Ranking
    # Top 15 candidates over 300 users
    def ranking_for_question(self, question_id):
        limit = 15  # let's work with 15 the top results only
        nb_of_users = 300
        results = map(lambda u: self.result(
            u, question_id), self.all_users()[:nb_of_users])
        return sorted(results, key=itemgetter(1), reverse=True)[:limit]
