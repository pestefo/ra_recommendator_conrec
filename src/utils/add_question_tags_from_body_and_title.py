#!/usr/bin/env python
# coding: utf-8
import sqlite3
from sqlite3 import Error
from collections import defaultdict
import re

conn = None
database = "data/v1.2.db"
tag_pattern = None
"""
Adding question tags from the body and the title of a question
We extract the text from a question and we create a json file
(like data/ros_question_tag.json) containing the tag ids
associated to a question.
"""


# BD

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    global conn
    try:
        conn = sqlite3.connect(db_file)
        print("dentro de create_connection")
        print(conn)
        return conn
    except Error as e:
        print(e)

    return None


def execute_query(query):
    global conn

    if not conn:
        create_connection(database)

    cur = conn.cursor()
    cur.execute(query)

    return cur.fetchall()


def get_data(question_id):
    query = "select title,summary from ros_question where id={}".format(
        question_id)
    return execute_query(query)[0]


def get_tags():
    query = "select name from ros_tag"
    return list(map(lambda x: x[0], execute_query(query)))


def get_question_ids():
    return [9084, 9097, 9107, 9130, 9135, 9159, 9163, 9166, 9208, 9210, 9259, 9261, 9273, 9287, 9343, 9471, 9511, 9512, 9545, 9553, 9588, 9637, 9640, 9686, 9693, 9766, 9768, 9807, 9815, 9902, 9922, 9942, 9943, 9977, 10026, 10027, 10038, 10047, 10110, 10120, 10130, 10143, 10145, 10166, 10187, 10222, 10245, 10329, 10332, 10335, 10338, 10343, 10356]


def extract_tags(str):
    global tag_pattern

    matches = re.findall(tag_pattern, str)

    for m in matches:
        print(m)

    return matches


def main():
    global tag_pattern
    # Question's Title and Body data

    # create a database connection
    conn = create_connection(database)

    questions = get_question_ids()
    tags = get_tags()
    extended_tags = defaultdict(set)

    tag_pattern = '(' + '|'.join(list(map(lambda x: re.escape(x), tags))) + ')'

    for q_id in questions[13:]:

        print("Question {}".format(q_id))

        title, body = get_data(q_id)
        print(title)
        extract_tags(title.lower())

        break

        extended_tags[q_id].append(extract_tags(title))
        # extended_tags[q_id].append(extract_tags(body))
        break

        bag_of_words = get_bag_of_words(body, title)

        register_extended_tags(q_id, bag_of_words)


if __name__ == '__main__':
    main()

'''
1. Faltan stopwords
2. kewas los lowerkase ermano

Question 9287
Are opencv samples in diamondback debs?
ar <---- ????
opencv
samples
in
diamondback
deb
'''