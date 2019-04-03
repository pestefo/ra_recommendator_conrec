#!/usr/bin/env python
# coding: utf-8
import sqlite3
from sqlite3 import Error
from collections import defaultdict, Counter
import re
import json

conn = None
database = "data/v1.2.db"
output_file = 'data/extended_tags.json'
tag_pattern = None
stopwords = list()

# Stopwords from https://gist.github.com/sebleier/554280
with open('src/utils/stopwords.txt', 'r') as fp:
    for line in fp:
        stopwords.append(line.rstrip())


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
    title, body = execute_query(query)[0]
    body = cleanhtml(body)
    return title, body


def get_tags():
    query = "select name from ros_tag"
    return list(map(lambda x: x[0], execute_query(query)))


def get_question_ids():
    return [9084, 9097, 9107, 9130, 9135, 9159, 9163, 9166, 9208, 9210, 9259, 9261, 9273, 9287, 9343, 9471, 9511, 9512, 9545, 9553, 9588, 9637, 9640, 9686, 9693, 9766, 9768, 9807, 9815, 9902, 9922, 9942, 9943, 9977, 10026, 10027, 10038, 10047, 10110, 10120, 10130, 10143, 10145, 10166, 10187, 10222, 10245, 10329, 10332, 10335, 10338, 10343, 10356]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def extract_tags(str):
    global tag_pattern, stopwords

    matches = re.findall(tag_pattern, str)

    matches = Counter(matches)

    # removing stopwords
    for tag in list(matches):
        if tag in stopwords:
            del matches[tag]

    return matches


def main():
    global tag_pattern, output_file
    # Question's Title and Body data

    # create a database connection
    conn = create_connection(database)

    questions = get_question_ids()
    tags = get_tags()
    extended_tags = defaultdict(list)

    tag_pattern = '\\b(' + \
        '|'.join(list(map(lambda x: re.escape(x), tags))) + ')\\b'

    for q_id in questions[13:]:

        print("Question {}".format(q_id))

        title, body = get_data(q_id)

        tags_found = extract_tags(title.lower())
        tags_found += extract_tags(body.lower())
        sorted(tags_found)

        print(tags_found.keys())
        extended_tags[q_id].extend(tags_found.keys())
        # extended_tags[q_id].append(extract_tags(body))

    with open(output_file, 'w') as outfile:
        json.dump(extended_tags, outfile)


if __name__ == '__main__':
    main()

'''
1. Faltan stopwords
2. kewas los lowerkase ermanz

Question 9287
Are opencv samples in diamondback debs?
ar <---- ????
opencv
samples
in
diamondback
deb
'''
