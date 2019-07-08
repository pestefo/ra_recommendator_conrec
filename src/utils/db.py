import mysql.connector


class Database:

    def __init__(self):

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

    def all_questions(self):
        if not self.QUESTIONS_CACHE:
            query = """
            SELECT distinct question_id
            from ra_question_tag"""

            self.execute (query, [])
            self.QUESTIONS_CACHE = list (map (lambda x: x[0],
                                              self.cursor.fetchall ()))

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

        self.execute(query, [])
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    def nb_of_questions(self):
        return len(self.all_questions())

    def all_users(self):

        if not self.USERS_CACHE:
            query = """
            SELECT distinct user_id
            from ra_user_tag"""

            self.execute(query, [])
            self.USERS_CACHE = list(map(lambda x: x[0],
                                        self.cursor.fetchall()))

        return self.USERS_CACHE

        # public - tag related

    def all_tags(self):
        """

        :return: dictionary with tag ids and their names
        :type dict of int -> str
        """

        if not self.TAGS_CACHE:

            query = """
            SELECT *
            from ra_tag"""

            self.execute (query, [])
            result = self.cursor.fetchall ()
            self.TAGS_CACHE = dict ()
            for pair in result:
                # tag_name : tag_id
                self.TAGS_CACHE[pair[1]] = pair[0]

        return self.TAGS_CACHE

    def all_tag_names(self):
        """

        :return: list of all tag names
        :type list of str
        """
        return list(self.all_tags().keys())

    def all_tag_ids(self):
        """

        :return: list of all tag ids
        :type list of int
        """
        return list(self.all_tags().values())

    def nb_of_tags(self):
        return len(self.all_tags())

    # TAGS and QUESTIONS

    def ros_answers_tag_names_for_question(self, question_id):
        query = """
            select ra_tag.name
            from ra_question_tag
            left join ra_tag on ra_question_tag.tag_id = ra_tag.id
            where ra_question_tag.question_id = {}""".format(question_id)

        self.execute(query, [])
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    def ros_answers_tag_ids_for_question(self, question_id):
        query = """
            select ra_tag.id
            from ra_question_tag
            left join ra_tag on ra_question_tag.tag_id = ra_tag.id
            where ra_question_tag.question_id = {}""".format(question_id)

        self.execute(query, [])
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    # TAGS and USERS

    def ros_answers_tag_names_for_user(self, user_id):
        query = """
            select ra_tag.name
            from ra_user_tag
            left join ra_tag on ra_user_tag.tag_id = ra_tag.id
            where ra_user_tag.user_id = {}""".format(user_id)

        self.execute(query, [])
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    def ros_answers_tag_ids_for_user(self, user_id):
        query = """
            select ra_tag.id
            from ra_user_tag
            left join ra_tag on ra_user_tag.tag_id = ra_tag.id
            where ra_user_tag.user_id = {}""".format(user_id)

        self.execute(query, [])
        return list(map(lambda x: x[0], self.cursor.fetchall()))

    # TAG Converters: id -> name | name -> id

    def tag_names_to_ids(self, list_of_tag_names):
        """
        It converts a list of taqs to a list of ids of those tags

        :param list_of_tag_names: list of tag strings
        :type list of str
        :return: list of tag ids
        :type list of int
        """
        # query = """
        # SELECT id
        # FROM ros_profiles_db.ra_tag
        # WHERE name in ({})
        # """.format ('\"' + '\",\"'.join (list_of_tag_names) + '\"')
        #
        # self.execute (query, [])
        # return list (map (lambda x: x[0],
        #                   self.cursor.fetchall ()))

        return list(map(lambda tag_name: self.TAGS_CACHE[tag_name], list_of_tag_names))

    def tag_ids_to_names(self, list_of_tag_ids):
        """
        It converts a list of taq ids to a list of names of those tags

        :param list_of_tag_ids: list of tag ids
        :type list of int
        :return: list of tag names
        :type list of str
        """
        query = """
        SELECT name
        FROM ros_profiles_db.ra_tag
        WHERE id in ({})
        """.format('\"' + '\",\"'.join(list_of_tag_ids) + '\"')

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

        # public - participation of users in questions (asking, answering or commenting)

    def participants_of_question(self, question_id):
        query = """
        select user_id
        from ros_question_participants
        where question_id={}   
        """.format(question_id)

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def questions_where_user_participated(self, user_id: int):
        """

        :param user_id: the identifier of the user
        :type int
        :return: list of question's ids in which the user has participated
        :type list of int
        """
        query = """
        select distinct question_id
        from ros_profiles_db.ros_question_participants
        where user_id = {}
        """.format(user_id)

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))

    def questions_described_using_the_ros_answers_tag_id(self, tag_id):
        query = """
        select question_id
        from ra_question_tag
        where tag_id = {}
        """.format(tag_id)

        self.execute(query, [])
        return list(map(lambda x: x[0],
                        self.cursor.fetchall()))
