import mysql.connector


class Database:

    def __init__(self, connection=None, scenario='B'):
        print("Initializing DB for scenario {}".format(scenario))

        self.host = 'localhost'
        self.user = 'root'
        self.password = 'buenacabr0s'
        self.db_name = 'ros_profiles_db'

        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.db_name,
            auth_plugin='mysql_native_password',
            use_unicode=True)

        self.cursor = self.connection.cursor()
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")
        self.cursor.execute("SET character_set_connection=utf8mb4")

        self.DB_TABLES = {
            "B": {"question_tag": "ra_question_tag_extended",
                  "user_tag": "ra_user_tag"},
            "C": {"question_tag": "ra_question_tag",
                  "user_tag": "ra_user_tag_extended"},
            "D": {"question_tag": "ra_question_tag_extended",
                  "user_tag": "ra_user_tag_extended"}
        }
        self.QUESTIONS_CACHE = None
        self.USERS_CACHE = None
        self.TAGS_CACHE = None

    def set_scenario(self, new_scenario):
        if new_scenario not in ('B', 'C', 'D'):
            raise Exception('Valid scenarios are "B", "C" or "D"')

        self.scenario = new_scenario

    def execute(self, query, data):
        self.cursor.execute(query, data)

    def commit(self):
        try:
            self.connection.commit()
        except Exception:
            self.connection.rollback()

    def tags_of_user(self, scenario, user_id):
        query = """
        select tag_id
        from {}
        where user_id={}""".format(
            self.DB_TABLES[scenario]['user_tag'],
            user_id)

        self.execute(query, [])

        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def tags_of_question(self, scenario, question_id):
        query = """
        select tag_id
        from {}
        where question_id={}""".format(
            self.DB_TABLES[scenario]['question_tag'],
            question_id)

        self.execute(query, [])

        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def questions_with_tag(self, scenario, tag_id):
        query = """
        select question_id
        from {}
        where tag_id={}""".format(
            self.DB_TABLES[scenario]['question_tag'],
            tag_id)

        self.execute(query, [])
        results = self.cursor.fetchall()
        results = list(map(lambda x: x[0], results))

        if not results:
            return []

        return results

    def all_questions(self):
        query = """
        select distinct question_id
        from ra_question_tag"""

        if not self.QUESTIONS_CACHE:
            self.execute(query, [])
            self.QUESTIONS_CACHE = list(map(lambda x: x[0],
                                            self.cursor.fetchall()))

        return self.QUESTIONS_CACHE

    def nb_of_questions(self):
        return len(self.all_questions())

    def all_users(self):
        query = """
        select distinct user_id
        from ra_user_tag"""

        if not self.USERS_CACHE:
            self.execute(query, [])
            self.USERS_CACHE = list(map(lambda x: x[0],
                                        self.cursor.fetchall()))

        return self.USERS_CACHE

    def all_tags(self):
        query = """
        select *
        from ra_tag"""

        if not self.TAGS_CACHE:
            self.execute(query, [])
            self.TAGS_CACHE = list(map(lambda x: x[0],
                                       self.cursor.fetchall()))

        return self.TAGS_CACHE

    def nb_of_tags(self):
        return len(self.all_tags())
