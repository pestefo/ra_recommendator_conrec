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
import src.utils.data_files as files
from src.algorithms.scenarios import Scenario
from src.algorithms.tag_map_based_algorithm import TMBAlgorithm
from src.utils.db import Database
from tqdm import tqdm

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

def main():

    r_ut = {}
    db = Database()

    for scenario in Scenario.all_scenarios():
        tmba = TMBAlgorithm(scenario)
        users = db.all_users()

        print("\n\n--- Starting R_ut Calculations for {} ---\n".format(scenario.name()))
        for user_id in tqdm(users):

            r_ut[user_id] = []

            for tag_id in tmba.tags_of_user(user_id):

                score = tmba.calculate_r_ut(user_id, tag_id)
                r_ut[user_id].append({"t": tag_id, "r": score})

        with open(files.r_ut_table_scenario[scenario.name()], 'w') as outfile:
            json.dump(r_ut, outfile)


if __name__ == '__main__':
    main()
