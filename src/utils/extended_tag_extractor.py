
from collections import defaultdict, Counter
import re
import json
import csv
import sqlite3
from sqlite3 import Error


class ExtendedTagExtractor:

    def __init__(self):
        self.__initialize_tag_pattern()
        self.__database = "data/v1.2.db"
        self.__create_connection()
        self.__initialize_stopwords()
        self.__initialize_tags()

    def __initialize_tag_pattern(self):
        self.tag_pattern = '\\b(' + \
            '|'.join(list(map(lambda x: re.escape(x),
                              self.__all_tags))) + ')\\b'

    def __initialize_stopwords(self):
        stopwords = list()
        # Stopwords from https://gist.github.com/sebleier/554280
        with open('src/utils/stopwords.txt', 'r') as fp:
            for line in fp:
                stopwords.append(line.rstrip())

        self.__stopwords = stopwords

    def __initialize_tags(self):
        query = "select name from ros_tag"
        return list(map(lambda x: x[0], self.__execute_query(query)))

    def __create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """

        try:
            self.__conn = sqlite3.connect(self.__database)
            return self.__conn
        except Error as e:
            print(e)

        return None

    def __execute_query(self, query):
        if not self.__conn:
            self.__create_connection(self.__database)

        cur = self.__conn.cursor()
        cur.execute(query)

        return cur.fetchall()

    def get_title_and_body(self, question_id):
        query = "select title,summary from ros_question where id={}".format(
            question_id)
        title, body = self.__execute_query(query)[0]
        body = self.__cleanhtml(body)
        return title, body

    def __extract_tags(self, str):

        matches = re.findall(self.tag_pattern, str)

        matches = Counter(matches)

        # removing stopwords
        for tag in list(matches):
            if tag in self.__stopwords:
                del matches[tag]

        return matches

    def extended_tags_for(self, question_id):
        title, body = self.get_title_and_body(question_id)

        tags_found = self.__extract_tags(title.lower())
        tags_found += self.__extract_tags(body.lower())

        sorted(tags_found)

        return tags_found
