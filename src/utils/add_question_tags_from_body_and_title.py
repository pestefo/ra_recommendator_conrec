#!/usr/bin/env python
# coding: utf-8
import sqlite3
from sqlite3 import Error

conn = None
database = "data/v1.2.db"
"""
Adding question tags from the body and the title of a question
We extract the text from a question and we create a json file
(like data/ros_question_tag.json) containing the tag ids
associated to a question.
"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def execute_query(field, question_id):
    if not conn:
        create_connection(database)

    cur = conn.cursor()
    cur.execute("select ? from ros_question where id=?", (field, question_id))

    return cur.fetchall()[0]


def get_body(question_id):
    return execute_query('body', question_id)


def get_title(question_id):
    return execute_query('title', question_id)


def get_question_ids():
    return [9084, 9097, 9107, 9130, 9135, 9159, 9163, 9166, 9208, 9210, 9259, 9261, 9273, 9287, 9343, 9471, 9511, 9512, 9545, 9553, 9588, 9637, 9640, 9686, 9693, 9766, 9768, 9807, 9815, 9902, 9922, 9942, 9943, 9977, 10026, 10027, 10038, 10047, 10110, 10120, 10130, 10143, 10145, 10166, 10187, 10222, 10245, 10329, 10332, 10335, 10338, 10343, 10356]


def find_tags_in_question(question_id):


def main():
    # Question's Title and Body data

    # create a database connection
    conn = create_connection(database)

    question_title_and_body_file = 'data/data_extracted_from_bd/ros_question_tag.json'
    with open(question_tags_file) as json_data:
        question_tags = json.load(json_data)

    question_tags_file = 'data/data_extracted_from_bd/ros_question_tag.json'
    question_tags = None
    extended_question_tags = None
    with open(question_tags_file) as json_data:
        question_tags = json.load(json_data)

    for q in get_question_ids[0]:
        extended_question_tags[q] = []
        extended_question_tags[q].extend(
            map(lambda n: int(n), question_tags[str(q)]))

        tags_found = find_tags_in_question(q)

        extended_question_tags[q].extend(tags_found)

    # dump extended_question_tags into a json file


if __name__ == '__main__':
    main()
