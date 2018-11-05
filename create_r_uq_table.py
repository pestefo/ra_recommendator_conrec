import sqlite3
import pandas as pd

act_ask = None
act_ans_comm = None
total_activities = None

r_uq_table_file = 'data/r_uq_2.json'
db_file = 'data/v1.db'
r_uq_csv_output_file = 'data/r_uq.csv'


def main():

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
        return total_activities[total_activities['ros_question_id'] ==
                                question_id]['total_activities'].values[0]

    # All users

    def all_users():
        return pd.concat([act_ans_comm['u_id'], act_ask['u_id']]).drop_duplicates()

    def all_questions():
        return pd.concat([act_ans_comm['q_id'], act_ask['q_id']]).drop_duplicates()

    # List of participants in a question - U_{q}

    def participants_of_question(question):
        answerers = act_ans_comm[(act_ans_comm['q_id'] == question) & (
            act_ans_comm['activity'] > 0)]["u_id"]
        askers = act_ask[(act_ask['q_id'] == question) &
                         (act_ask['activity'] > 0)]["u_id"]
        return pd.concat([answerers, askers]).drop_duplicates()

    # Activity

    def activity(user, question):
        return activity_ans_comm(user, question) + activity_ask(user, question)

    def r_uq(user, question):
        if activity(user, question) == 0:
            return 0
        return activity(user, question) / question_activities(question)

    conn = sqlite3.connect(db_file)

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
    act_ans_comm = pd.read_sql_query(query_activity_ans_comm, conn)

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
    act_ask = pd.read_sql_query(query_activity_ask, conn)

    # Total nb of activities per question
    query_total_activities = """
    select ros_question_id, count(*)+1 as total_activities
    from ros_question_answer
    group by ros_question_id
    """
    total_activities = pd.read_sql_query(query_total_activities, conn)

    conn.close()

    # Create table of R_uq
    questions = all_questions()
    # users = all_users()
    import csv
    with open(r_uq_csv_output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for q in questions:
            for u in participants_of_question(q):
                r = r_uq(u, q)
                print("u:" + str(u) + "\tq:" + str(q) + "\t" + str(r))
                writer.writerow([u, q, r])


if __name__ == '__main__':
    main()
