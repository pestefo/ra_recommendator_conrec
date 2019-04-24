'''
Data of ros_user_tag.csv, ros_tag.csv and ros_question_tag.csv
were extracted from with simple SELECT * FROM table queries

NOTE:
This tables have question-tag and user-tag associations given
from ROS Answers.
I would like to enrich this user and question tag characterization
by adding tags extracted as keywords of question body or title, or
GitHub repositories description of users,

'''
import json
import data_files as files
from db import Database
from math import log
"""
From
2,3,5
2,4,6
3,1,2
4,5,6
4,6,7

To:
2: [(3,5),(4,6)],
3:[2,1],
4:[(5,6).(6,7)],...
"""

r_uq_data = files.get_data(files.r_uq_table)

tag_dict = None
db = Database()
db_tables = {
    "B": {"question_tag": "ra_question_tag_extended",
          "user_tag": "ra_user_tag"},
    "C": {"question_tag": "ra_question_tag",
          "user_tag": "ra_user_tag_extended"},
    "D": {"question_tag": "ra_question_tag_extended",
          "user_tag": "ra_user_tag_extended"}
}

output_file = {
    "B": 'r_ut_scenario_b.json',
    "C": 'r_ut_scenario_c.json',
    "D": 'r_ut_scenario_d.json',
}

questions = None


def tags_of_user(table, user_id):
    query = """
    select tag_id
    from {}
    where user_id={}""".format(table, user_id)
    db.execute(query, [])
    results = db.cursor.fetchall()

    return list(map(lambda x: x[0], results))


def questions_with_tag(table, tag_id):
    query = """
    select question_id
    from {}
    where tag_id={}""".format(table, tag_id)
    # print(query)
    db.execute(query, [])
    results = db.cursor.fetchall()
    results = list(map(lambda x: x[0], results))
    if not results:
        return []
    return results


def all_questions():
    global questions

    query = """
    select distinct question_id
    from ra_question_tag"""

    if not questions:
        db.execute(query, [])
        questions = db.cursor.fetchall()

    return list(map(lambda x: x[0], questions))


def nb_of_questions():
    return len(all_questions())


def r_uq(user_id, question_id):
    try:
        pairs = r_uq_data[str(question_id)]
        for p in pairs:
            if p['u'] == user_id:
                return p['r']

    # If there's no calculated R_uq for that user_id and question_id
    # it means that user_id did not participate in question_id, then,
    # r_uq(user_id, question_id) = 0
    # print("user_id={}\tquestion_id={}".format(user_id, question_id))
    except Exception:
        return 0

    return 0

def all_users():
    query = """
    select distinct user_id
    from ra_user_tag"""
    db.execute(query, [])
    results = db.cursor.fetchall()

    return list(map(lambda x: x[0], results))


def calculate_r_ut(user_id, tag_id, question_table):
    questions = questions_with_tag(question_table, tag_id)
    # TODO: In theory, this should never happen
    if len(questions) == 0:
        return 0
    log_of_ratio = log(nb_of_questions() / len(questions))
    return log_of_ratio * sum(map(lambda q: r_uq(user_id, q),
                                  questions))


def main():
    import datetime

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    # Create table of R_ut

    r_ut = {}

    users = all_users()
    scenarios = ['B', 'C', 'D']
    for scenario in scenarios[1:]:
        question_table = db_tables[scenario]['question_tag']
        user_table = db_tables[scenario]['user_tag']

        for u in users:
            print("------- start (" + scenario + ") -------")
            print("user: " + str(u))
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S'))

            r_ut[u] = []

            for t in tags_of_user(user_table, u):
                # print("tag: " + str(t))
                r = calculate_r_ut(u, t, question_table)
                # print("u:" + str(u) + "\tt:" + str(t) + "\t" + str(r))
                r_ut[u].append({"t": t, "r": r})

            print("\n" + str((datetime.datetime.now() - now).seconds) +
                  " seconds")
            print("------- end -------\n\n")

        with open(output_file[scenario], 'w') as outfile:
            json.dump(r_ut, outfile)


if __name__ == '__main__':
    main()
