#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from math import sqrt
from operator import itemgetter, attrgetter


class ConRec:

    path_to_db = "v1.db"

    act_ans_comm = None
    act_ask = None
    total_activities = None

    def __init__(self, name, salary):
        self.extract_data_from_db()

    def extract_data_from_db(self):
        import sqlite3
        conn = sqlite3.connect("v1.db")

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

        ConRec.act_ask = pd.read_sql_query(query_activity_ask, conn)
        ConRec.act_ans_comm = pd.read_sql_query(query_activity_ans_comm, conn)
        ConRec.total_activities = pd.read_sql_query(
            query_total_activities, conn)

        conn.close()

    def activity_ans_comm(user_id, question_id):
        val = act_ans_comm[(act_ans_comm['u_id'] == user_id) & (
            act_ans_comm['q_id'] == question_id)]["activity"]
        if val.empty:
            return 0
        return val.values[0]

    def activity_ask(user_id, question_id):
        val = act_ask[(act_ask['u_id'] == user_id) & (
            act_ask['q_id'] == question_id)]["activity"]
        if val.empty:
            return 0
        return val.values[0]

    def question_activities(question_id):
        return total_activities[total_activities['ros_question_id'] == question_id]["total_activities"].values[0]

    # In[6]:

    def all_users():
        return pd.concat([act_ans_comm['u_id'], act_ask['u_id']]).drop_duplicates()

    # Activity

    def activity(user, question):
        return activity_ans_comm(user, question) + activity_ask(user, question)

    # List of participants in a question - U_{q}

    def participants_of_question(question):
        answerers = act_ans_comm[(act_ans_comm['q_id'] == question) & (
            act_ans_comm['activity'] > 0)]["u_id"]
        askers = act_ask[(act_ask['q_id'] == question) &
                         (act_ask['activity'] > 0)]["u_id"]
        return pd.concat([answerers, askers]).drop_duplicates()

    def questions_for_user(user):
        questions_answered = act_ans_comm[(act_ans_comm['u_id'] == user) & (
            act_ans_comm['activity'] > 0)]["q_id"]
        questions_asked = act_ask[(act_ask['u_id'] == user) & (
            act_ask['activity'] > 0)]["q_id"]
        return set(pd.concat([questions_answered, questions_asked]).drop_duplicates())

    def questions_in_common(users):
        questions = questions_for_user(users[0])
        for user in users[1:]:
            questions &= questions_for_user(user)
            if not questions:
                return set()
        return questions

    # In[20]:

    # Importing R_uq table - http://www.convertcsv.com/csv-to-json.htm
    #r_uq_table = pd.read_csv('r_uq.csv', sep='\t')
    import json
    with open('r_uq_2.json') as json_data:
        r_uq_table = json.load(json_data)

    # Relation between a user and a question
    def r_uq(user, question):
        #val = r_uq_table[(r_uq_table['u'] == user) & (r_uq_table['q'] == question)]['r']
        try:
            return r_uq_table[str(question)][str(user)]
        except KeyError as e:
            cause = e.args[0]
            if cause == str(question):
                print("Question " + str(cause) + " doesn't exist.")
                return -1

            print("User " + str(cause) +
                  " hasn't any activity in question " + str(question) + ".")
            return 0

    # Old implementation

    def calculate_r_uq(user, question):
        if activity(user, question) == 0:
            return 0
        return activity(user, question) / question_activities(question)

    # Relation between two users
    def r_uu(user_a, user_b):
        a = sum(map(lambda q: r_uq(user_a, q) * r_uq(user_b, q),
                    questions_in_common([user_a, user_b])))
        b = sqrt(sum(map(lambda q: r_uq(user_a, q)**2, questions_for_user(user_a)))
                 * sum(map(lambda q: r_uq(user_b, q)**2, questions_for_user(user_b))))
        if a == 0:
            return 0
        return a / b

    def result(user, question):
        return user, sum(map(lambda u: r_uq(u, question) * r_uu(user, u), participants_of_question(question)))

    # TODO: Remove limit!!!!
    def ranking_for_question(question):
        limit = 15  # let's work with 15 the top results only
        results = map(lambda u: result(u, question), all_users()[:300])
        return sorted(results, key=itemgetter(1), reverse=True)[:limit]

    def example(self):

        # Tests for activity_ans_comm
        #print("\nTests: activity_ans_comm")
        # print("-----")
        #print(activity_ans_comm(0,9045) == 0)
        #print(activity_ans_comm(3,9045) == 1)
        #print(activity_ans_comm(23668,9045) == 2)
            # Tests for activity_task
        #print("\nTests: activity_task")
        # print("-----")
        # print("activity_ask(7,9045) == 1\t"+str(activity_ask(7,9045) == 1)) # True
        # print("activity_ask(3,9045) == 0\t"+str(activity_ask(3,9045) == 0)) # True
        # print("activity_ask(23668,9045) == 0\t"+str(activity_ask(23668,9045) == 0)) # True
            # Tests for question_activities
        #print("\nTests: question_activities")
        # print("-----")
        # print("question_activities(9033) == 4\t\t"+str(question_activities(9033) == 4)) # True
        # print("question_activities(9190) == 14\t\t"+str(question_activities(9190) == 14)) # True
        # print("question_activities(236154) == 9\t"+str(question_activities(236154) == 9)) # True
            #print("Question ID: 9045")
        # print("-----------------")
        #print("Asker ID = 7, Answers/Commenters = 3, 5184, 23668")
        # print(participants_of_question(9045))

        # List of questions in which a user participates - Q_{u}

            # print("")
        # print("# Questions for user 7\t\t: "+str(len(questions_for_user(7)))) # participated: 2520,
        # print("# Questions for user 3\t\t: "+str(len(questions_for_user(3))))
        # print("# Questions for user 5184\t: "+str(len(questions_for_user(5184))))
        #print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(set(questions_for_user(23668)) & set(questions_for_user(5184)) & set(questions_for_user(3)) & set(questions_for_user(7))))
        #print("Users 3, 5184, 23668 and 7 participated in Q 9045 --> "+str(questions_in_common([3, 5184, 23668, 7])))
        #print("Users 3, and 7 --> "+str(questions_in_common([3, 7])))
            #print(" ")
    print("Relation user-question (r_uq)")
    print("Asker\t\t:\tr_uq(7,9045)= " + str(r_uq(7, 9045)))
    print("Answerer\t:\tr_uq(3,9045)= " + str(r_uq(3, 9045)) +
          " (provides the accepted answer)")
    print("Participant\t:\tr_uq(5184,9045)= " +
          str(r_uq(5184, 9045)) + " (participated twice)")
    #print(" ")
    print("Relation user-user (r_uu)")
    print("Asker-Answerer\t\t:\tr_uu(7,3)= " + str(r_uu(7, 3)))
    print("Asker-Participant\t:\tr_uu(7,5184)= " + str(r_uu(7, 5184)))
    print("Answerer-Participant\t:\tr_uu(3,5184)= " + str(r_uu(5184, 3)))

    # -----
        show_tests = True

        if show_tests:
            print(" ")
            print("Results for Q_id=9045")
            print("Asker\t\t:\tresult(7,9045)= " + str(result(7, 9045)))
            print("Answerer\t:\tresult(3,9045)= " +
                  str(result(3, 9045)) + " (provides the accepted answer)")
            print("Participant\t:\tresult(5184,9045)= " +
                  str(result(5184, 9045)) + " (participated twice)")

            # -----
        show_ranking = True

        if show_ranking:
            print(" ")
            print("Ranking for q=9045")
            print("------------------")
            print(str(ranking_for_question(9045)))
            for result in ranking_for_question(9045):
                print(str(result[0]) + " - " + str(result[1]))
