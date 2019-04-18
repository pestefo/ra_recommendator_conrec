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
import csv
import json
from algorithms.tag_map_based_algorithm import TMBAlgorithm
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

tag_dict = None


r_ut_output_file = 'data/r_ut_questions_extended.json'


def main():
    import datetime

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    # Create table of R_ut
    tmba = TMBAlgorithm()
    users = tmba.all_users()
    r_ut = {}

    for u in users:
        print("------- start -------")
        print("user: " + str(u))
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        r_ut[u] = []

        for t in tmba.tags_of_user(u):
            r = tmba.calculate_r_ut(u, t)
            # print("u:" + str(u) + "\tt:" + str(t) + "\t" + str(r))
            r_ut[u].append({"t": t, "r": r})

        print("\n" + str((datetime.datetime.now() - now).seconds) + " seconds")
        print("------- end -------\n\n")

    with open(r_ut_output_file, 'w') as outfile:
        json.dump(r_ut, outfile)


if __name__ == '__main__':
    main()
