import json
import sqlite3
from random import shuffle

from tqdm import tqdm

import src.utils.data_files as files
from src.utils.db import Database
from src.utils.extended_tag_extractor import QuestionTagExtractor

"""
Here we populate a dictionary with users and their full list of extended tags (i.e. tags from RA and full extended
tags from the questions in which the user has previously participated), eg.

"2" : [1321,4523,65,343,432]
"""


def extract_extended_tags_for_users():
    db = Database ()
    tag_extractor = QuestionTagExtractor ()
    user_tags = {}

    users = db.all_users ()
    shuffle (users)
    print ("Extracting tags...\n")
    for user in tqdm (users):
        user_tags[user] = set ()
        questions = db.questions_where_user_participated (user)
        for question in questions:
            try:
                user_tags[user] = user_tags[user].union (tag_extractor.full_extended_tag_ids_for (question))
            except sqlite3.OperationalError:
                print ("Operantional ERROR on question: {} \t user: {}".format (question, user))

        user_tags[user] = list (user_tags[user])

    print ("DONE\n")
    with open (files.user_full_extended_tags, 'w') as fp:
        json.dump (user_tags, fp)


def extract_extended_tags_for_questions():
    db = Database ()
    tag_extractor = QuestionTagExtractor ()
    question_tags = {}

    questions = db.all_questions ()

    print ("Extracting tags...\n")
    for question in tqdm (questions):
        question_tags[question] = []
        try:
            question_tags[question] = list (tag_extractor.full_extended_tag_ids_for (question))
        except sqlite3.OperationalError:
            print ("Operantional ERROR on question: {} ".format (question))

    print ("DONE\n")

    with open (files.question_full_extended_tags, 'w') as fp:
        json.dump (question_tags, fp)

def invert_dict(d):
    inverse = dict()
    for key in tqdm(d):
        # Go through the list that is saved in the dict:
        for item in d[key]:
            # Check if in the inverted dict the key exists
            if item not in inverse:
                # If not create a new list
                inverse[item] = [key]
            else:
                inverse[item].append(key)
    return inverse

def reversing_the_extended_tags_for_questions_dictionary():
    with open(files.question_full_extended_tags, 'r') as fp:
        d = json.load(fp)
    tags_to_questions = invert_dict(d)

    with open (files.full_extended_tags_to_questions, 'w') as fp:
        json.dump (tags_to_questions, fp)


def main():
    pass




if __name__ == '__main__':
    main ()
