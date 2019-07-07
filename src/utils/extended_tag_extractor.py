import json
from collections import Counter
import re
import sqlite3
from sqlite3 import Error
import src.utils.data_files as files
from src.utils.db import Database


class QuestionTagExtractor:

    # private - initialization

    def __init__(self):
        self.__mysqldb = Database()
        self.__sqlite3db_conn = self.__create_connection()
        self.__initialize_tags()
        self.__initialize_tag_pattern()
        self.__initialize_stopwords()

    def __create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :return: Connection object or None
        """

        try:
            self.__sqlite3db_conn = sqlite3.connect(files.db)
            return self.__sqlite3db_conn

        except Error as e:
            print(e)

        return None

    def __initialize_tag_pattern(self):
        self.tag_pattern = '\\b(' + \
                           '|'.join(list(map(lambda x: re.escape(x),
                                             self.__all_tags))) + ')\\b'

    def __initialize_stopwords(self):
        stopwords = list()
        # Stopwords from https://gist.github.com/sebleier/554280
        for f in files.stopwords:
            with open(f, 'r') as fp:
                for line in fp:
                    stopwords.append(line.rstrip())

        self.__stopwords = stopwords

    def __initialize_tags(self):
        self.__all_tags = self.__mysqldb.all_tag_names()

    # private - Sqlite3 db

    def __execute_sqlite3_query(self, query):
        if not self.__sqlite3db_conn:
            self.__create_connection()

        cur = self.__sqlite3db_conn.cursor()
        cur.execute(query)

        return cur.fetchall()

    # private - core

    def __extract_tags(self, str):

        matches = re.findall(self.tag_pattern, str)

        matches = Counter(matches)

        # removing stopwords
        for tag in list(matches):
            if tag in self.__stopwords or tag.isdigit():
                del matches[tag]

        return matches

    def __cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    # public methods

    def ros_answers_tags_for(self, question_id):
        """
        Returns the tags that were entered by the authors of the question

        :param question_id: the id of a question
        :type int
        :return: a list of tag names obtained from the ROS Answers' website
        :type list of str
        """

        return self.__mysqldb.ros_answers_tag_names_for_question(question_id)

    def ros_answers_tag_ids_for(self, question_id):
        return self.__mysqldb.ros_answers_tag_ids_for_question(question_id)

    def extracted_tags_for(self, question_id):
        """
        Returns both Extended Tags and User entered tags

        :param question_id: the id of a question
        :type int
        :return: a list of tag names obtained from the extended tags and the user entered tags
        :type list of str
        """
        return list(self.count_of_tags_for(question_id).keys())

    def extracted_tag_ids_for(self, question_id):
        return self.tag_names_to_ids(self.extracted_tags_for(question_id))

    def full_extended_tags_for(self, question_id):
        """
        Returns both Extended Tags and User entered tags

        :param question_id: the id of a question
        :type int
        :return: a list of tag names obtained from the extended tags and the user entered tags
        :type list of str
        """
        return list(set(self.ros_answers_tags_for(question_id)).union(set(self.extracted_tags_for(question_id))))

    def full_extended_tag_ids_for(self, question_id):

        return set(self.ros_answers_tag_ids_for(question_id)).union(self.extracted_tag_ids_for(question_id))

    def count_of_tags_for(self, question_id):
        title, body = self.get_title_and_body(question_id)
        tags_found = self.__extract_tags(title.lower())
        tags_found += self.__extract_tags(body.lower())
        sorted(tags_found)
        return tags_found

    def get_title_and_body(self, question_id):
        """

        :param question_id: id of a question
        :type int
        :return: a tuple containing the title and body string of the question
        :type (str, str)
        """
        query = "select title,summary from ros_question where id={}".format(
            question_id)
        title, body = self.__execute_sqlite3_query(query)[0]
        body = self.__cleanhtml(body)
        return title, body

    def body_extended_tags_for(self, question_id):
        """

        :param question_id: id of a question
        :type int
        :return: list of tags found in the question's body
        :type list of str
        """
        title, body = self.get_title_and_body(question_id)

        tags_found = self.__extract_tags(body.lower())

        sorted(tags_found)

        return tags_found

    def title_extended_tags_for(self, question_id):
        """

        :param question_id: id of a question
        :type int
        :return: list of tags found in the question's title
        :type list of str
        """
        title, body = self.get_title_and_body(question_id)

        tags_found = self.__extract_tags(title.lower())

        sorted(tags_found)

        return tags_found

    def tag_ids_to_names(self, list_of_tag_ids):
        """

        :param list_of_tag_ids: list of tag ids
        :type list of int
        :return: list of tag names
        :type list of str
        """
        return self.__mysqldb.tag_ids_to_names(list_of_tag_ids)

    def tag_names_to_ids(self, list_of_tag_names):
        """

        :param list_of_tag_names: list of tag names
        :type list of str
        :return: list of tag ids
        :type list of int
        """
        return self.__mysqldb.tag_names_to_ids(list_of_tag_names)
