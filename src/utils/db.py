import mysql.connector


class Database:

    def __init__(self, connection=None, scenario='B'):
        print("Initializing DB for scenario {}".format(scenario))

        self.host = 'localhost'
        self.user = 'root'
        self.password = 'buenacabr0s'
        self.self_name = 'ros_profiles_self'

        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.self_name,
            auth_plugin='mysql_native_password',
            use_unicode=True)

        self.cursor = self.connection.cursor()
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute("SET CHARACTER SET utf8mb4")
        self.cursor.execute("SET character_set_connection=utf8mb4")

        # with open(files.tables, 'r') as fp:
        #     self.tables = json.load(fp)

        self.db_tables = {
            "B": {"question_tag": "ra_question_tag_extended",
                  "user_tag": "ra_user_tag"},
            "C": {"question_tag": "ra_question_tag",
                  "user_tag": "ra_user_tag_extended"},
            "D": {"question_tag": "ra_question_tag_extended",
                  "user_tag": "ra_user_tag_extended"}
        }
        self.questions = None

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
        where user_id={}""".format(self.db_tables[scenario]['user_tag'], user_id)
        self.execute(query, [])
        results = self.cursor.fetchall()

        return list(map(lambda x: x[0], results))

    def tags_of_question(self, scenario, question_id):
        query = """
        select tag_id
        from {}
        where question_id={}""".format(self.db_tables[scenario]['question_tag'], user_id)
        self.execute(query, [])
        results = self.cursor.fetchall()

        return list(map(lambda x: x[0], results))

    def questions_with_tag(self, scenario, tag_id):
        query = """
        select question_id
        from {}
        where tag_id={}""".format(self.db_tables[scenario]['question_tag'], tag_id)
        # print(query)
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

        if not self.questions:
            self.execute(query, [])
            self.questions = self.cursor.fetchall()

        return list(map(lambda x: x[0], self.questions))

    def nb_of_questions(self):
        return len(self.all_questions())

    def all_users(self):
        query = """
        select distinct user_id
        from ra_user_tag"""
        self.execute(query, [])
        results = self.cursor.fetchall()

        return list(map(lambda x: x[0], results))
