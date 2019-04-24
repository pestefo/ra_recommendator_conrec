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
from math import log, floor
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

OUTPUT_FILE = files.r_ut_table_scenario
db = None


def tags_of_user(scenario, user_id):
    global db
    return db.tags_of_user(scenario, user_id)


def questions_with_tag(scenario, tag_id):
    global db
    return db.questions_with_tag(scenario, tag_id)


def all_questions():
    global db
    return db.all_questions()


def nb_of_questions():
    global db
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

    except Exception:
        return 0

    return 0


def all_users():
    global db
    return db.all_users()


def calculate_r_ut(user_id, tag_id, scenario):
    questions = questions_with_tag(scenario, tag_id)

    if len(questions) == 0:
        return 0

    log_of_ratio = log(nb_of_questions() / len(questions))
    return log_of_ratio * sum(map(lambda q: r_uq(user_id, q),
                                  questions))


def print_progress(current_progress):
    STEPS = range(0, 5, 100)
    if current_progress * 100 in STEPS:
        print("Progress: {}\%".progress)


def main():
    import datetime
    global db

    r_ut = {}
    SCENARIOS = ['B', 'C', 'D']

    for scenario in SCENARIOS:
        print("------- start (" + scenario + ") -------")
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        db = Database(scenario)
        users = all_users()

        for u in users:

            print_progress(floor(int(u) / len(users)))
            # print("------- start (" + scenario + ") -------")
            # print("user: " + str(u))

            r_ut[u] = []

            for t in tags_of_user(scenario, u):
                # print("tag: " + str(t))
                r = calculate_r_ut(u, t, scenario)
                # print("u:" + str(u) + "\tt:" + str(t) + "\t" + str(r))
                r_ut[u].append({"t": t, "r": r})

            print("\n" + str((datetime.datetime.now() - now).seconds) +
                  " seconds")

        with open(OUTPUT_FILE[scenario], 'w') as outfile:
            json.dump(r_ut, outfile)

        print("------- end -------\n\n")


if __name__ == '__main__':
    main()
