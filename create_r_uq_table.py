import sqlite3
import pandas as pd

act_ask = None
act_ans_comm = None
total_activities = None


def activity_ans_comm(user_id, question_id):
    val = act_ans_comm[(act_ans_comm['u_id'] == user_id) & (
        act_ans_comm['q_id'] == question_id)]["activity"]
    if val.empty:
        return 0
    return val.values[0]


# Tests for activity_ans_comm
# print("\nTests: activity_ans_comm")
# print("-----")
# print(activity_ans_comm(0, 9045) == 0)
# print(activity_ans_comm(3, 9045) == 1)
# print(activity_ans_comm(23668, 9045) == 2)


def activity_ask(user_id, question_id):
    val = act_ask[(act_ask['u_id'] == user_id) & (
        act_ask['q_id'] == question_id)]["activity"]
    if val.empty:
        return 0
    return val.values[0]


# Tests for activity_task
# print("\nTests: activity_task")
# print("-----")
# print("activity_ask(7,9045) == 1\t" + str(activity_ask(7, 9045) == 1))  # True
# print("activity_ask(3,9045) == 0\t" + str(activity_ask(3, 9045) == 0))  # True
# print("activity_ask(23668,9045) == 0\t" +
#       str(activity_ask(23668, 9045) == 0))  # True


def question_activities(question_id):
    return total_activities[total_activities['ros_question_id'] == question_id]["total_activities"].values[0]


# Tests for question_activities
print("\nTests: question_activities")
print("-----")
print("question_activities(9033) == 4\t\t" +
      str(question_activities(9033) == 4))  # True
print("question_activities(9190) == 14\t\t" +
      str(question_activities(9190) == 14))  # True
print("question_activities(236154) == 9\t" +
      str(question_activities(236154) == 9))  # True

# All users


def all_users():
    return pd.concat([act_ans_comm['u_id'], act_ask['u_id']]).drop_duplicates()

# Activity


def activity(user, question):
    return activity_ans_comm(user, question) + activity_ask(user, question)


def r_uq(user, question):
    if activity(user, question) == 0:
        return 0
    return activity(user, question) / question_activities(question)


def main():

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
    questions = Set(act_ans_comm['q_id']) & Set(act_ask['q_id']).apply(list)

    for q in questions:
        

if __name__ == '__main__':
    main()
