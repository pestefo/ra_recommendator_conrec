
from collections import Counter
import re
import sqlite3
from sqlite3 import Error
import src.utils.data_files as files

# Ejecutar desde ../src para evitar problemas de paths


class ExtendedTagExtractor:

    # private - initialization

    def __init__(self):
        self.__database = files.db
        self.__conn = self.__create_connection()
        self.__initialize_tags()
        self.__initialize_tag_pattern()
        self.__initialize_stopwords()

    def __initialize_tag_pattern(self):
        self.tag_pattern = '\\b(' + \
            '|'.join(list(map(lambda x: re.escape(x),
                              self.__all_tags))) + ')\\b'

    def __initialize_stopwords(self):
        stopwords = list()
        # Stopwords from https://gist.github.com/sebleier/554280
        with open(files.stopwords, 'r') as fp:
            for line in fp:
                stopwords.append(line.rstrip())

        self.__stopwords = stopwords

    def __initialize_tags(self):
        query = "select name from ros_tag"
        self.__all_tags = list(
            map(lambda x: x[0], self.__execute_query(query)))

    def __create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :return: Connection object or None
        """

        try:
            self.__conn = sqlite3.connect(self.__database)
            return self.__conn

        except Error as e:
            print(e)

        return None

    # private -db

    def __execute_query(self, query):
        if not self.__conn:
            self.__create_connection()

        cur = self.__conn.cursor()
        cur.execute(query)

        return cur.fetchall()

    # private - core

    def __extract_tags(self, str):

        matches = re.findall(self.tag_pattern, str)

        matches = Counter(matches)

        # removing stopwords
        for tag in list(matches):
            if tag in self.__stopwords:
                del matches[tag]

        return matches

    def __cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    # public methods
    def tags_for(self, question_id):
        # Returns the tags that were entered by the authors of the question
        query = """
            select ros_tag.name
            from ros_question_tag
            left join ros_tag on ros_question_tag.ros_tag_id = ros_tag.id
            where ros_question_tag.ros_question_id = {}""".format(question_id)
        tags = self.__execute_query(query)

        return list(map(lambda x: x[0], tags))

    def get_title_and_body(self, question_id):
        query = "select title,summary from ros_question where id={}".format(
            question_id)
        title, body = self.__execute_query(query)[0]
        body = self.__cleanhtml(body)
        return title, body

    def extended_tags_for(self, question_id):
        return list(self.count_of_tags_for(question_id).keys())

    def count_of_tags_for(self, question_id):
        title, body = self.get_title_and_body(question_id)
        tags_found = self.__extract_tags(title.lower())
        tags_found += self.__extract_tags(body.lower())
        sorted(tags_found)
        return tags_found

    def body_extended_tags_for(self, question_id):
        title, body = self.get_title_and_body(question_id)

        tags_found = self.__extract_tags(body.lower())

        sorted(tags_found)

        return tags_found

    def title_extended_tags_for(self, question_id):
        title, body = self.get_title_and_body(question_id)

        tags_found = self.__extract_tags(title.lower())

        sorted(tags_found)

        return tags_found
