import json
import sqlite3

from tqdm import tqdm
import src.utils.data_files as files
from src.utils.db import Database
from src.utils.extended_tag_extractor import QuestionTagsContainer
from random import shuffle
"""
Here we populate a dictionary with users and their full list of extended tags (i.e. tags from RA and full extended
tags from the questions in which the user has previously participated), eg.

"2" : [1321,4523,65,343,432]
"""

def extract_extended_tags_for_users():
    db = Database ("A")
    tag_extractor = QuestionTagsContainer ()
    user_tags = {}

    users = db.all_users ()
    shuffle(users)
    print ("Extracting tags...\n")
    for user in tqdm(users):
        user_tags[user] = set ()
        questions = db.questions_where_user_participated (user)
        for question in questions:
            try:
                user_tags[user] = user_tags[user].union (tag_extractor.full_extended_tag_ids_for (question))
            except sqlite3.OperationalError:
                print("Operantional ERROR on question: {} \t user: {}".format(question,user))

        user_tags[user] = list(user_tags[user])

    print ("DONE\n")
    with open (files.user_full_extended_tags, 'w') as fp:
        json.dump (user_tags, fp)

def main():
    db = Database ("A")
    tag_extractor = QuestionTagsContainer ()
    question_tags = {}

    questions = db.all_questions ()

    print ("Extracting tags...\n")
    for question in tqdm(questions):
        question_tags[question] = []
        try:
            question_tags[question] = list(tag_extractor.full_extended_tag_ids_for (question))
        except sqlite3.OperationalError:
            print("Operantional ERROR on question: {} ".format(question))

    print ("DONE\n")

    with open (files.question_full_extended_tags, 'w') as fp:
        json.dump (question_tags, fp)


if __name__ == '__main__':
    main ()
