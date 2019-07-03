import mysql.connector


class Database:

    def __init__(self, scenario, connection=None, ):

        self.scenario = scenario

        print("Initializing DB for scenario {}...".format(self.scenario))

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
            "A": {"question_tag": "ra_question_tag",
                  "user_tag": "ra_user_tag"},
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

    def execute(self, query, data):
        self.cursor.execute(query, data)

    def commit(self):
        try:
            self.connection.commit()
        except Exception:
            self.connection.rollback()

    def tags_of_user(self, user_id):
        query = """
        SELECT tag_id
        from {}
        where user_id={}""".format(
            self.DB_TABLES[self.scenario]['user_tag'],
            user_id)

        self.execute(query, [])

        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def tags_of_question(self, question_id):
        query = """
        SELECT tag_id
        from {}
        where question_id={}""".format(
            self.DB_TABLES[self.scenario]['question_tag'],
            question_id)

        self.execute(query, [])

        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def questions_with_tag(self, tag_id):
        query = """
        SELECT question_id
        from {}
        where tag_id={}""".format(
            self.DB_TABLES[self.scenario]['question_tag'],
            tag_id)

        self.execute(query, [])
        results = self.cursor.fetchall()
        results = list(map(lambda x: x[0], results))

        if not results:
            return []

        return results

    def all_questions(self):
        query = """
        SELECT distinct question_id
        from ra_question_tag"""

        if not self.QUESTIONS_CACHE:
            self.execute(query, [])
            self.QUESTIONS_CACHE = list(map(lambda x: x[0],
                                            self.cursor.fetchall()))

        return self.QUESTIONS_CACHE

    def questions_with_n_participants(self, nb_of_participants):
        query = """
        select question_id 
        from
           (
              SELECT
                 question_id,
                 count(distinct user_id) as nb_of_participants 
              FROM
                 ros_profiles_db.ros_question_participants 
              group by
                 question_id
           )
           as summarized 
        where summarized.nb_of_participants = {}""".format(nb_of_participants)

        self.execute (query, [])
        return list (map (lambda x: x[0], self.cursor.fetchall ()))

    def nb_of_questions(self):
        return len(self.all_questions())

    def all_users(self):
        query = """
        SELECT distinct user_id
        from ra_user_tag"""

        if not self.USERS_CACHE:
            self.execute(query, [])
            self.USERS_CACHE = list(map(lambda x: x[0],
                                        self.cursor.fetchall()))

        return self.USERS_CACHE

    def all_tags(self):
        query = """
        SELECT *
        from ra_tag"""

        if not self.TAGS_CACHE:
            self.execute(query, [])
            self.TAGS_CACHE = list(map(lambda x: x[0],
                                       self.cursor.fetchall()))

        return self.TAGS_CACHE

    def nb_of_tags(self):
        return len(self.all_tags())

    def participants_of_question(self, question_id):
        query = """
        select user_id
        from ros_question_participants
        where question_id={}   
        """.format(question_id)

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def questions_where_user_participated(self, user_id):
        query = """
        select distinct question_id
        from ros_profiles_db.ros_question_participants
        where user_id = {}
        """.format(user_id)

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))
