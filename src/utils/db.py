import mysql.connector
import json
import data_files as files


class Database:

    def __init__(self, connection=None):
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

        with open(files.tables, 'r') as fp:
            self.tables = json.load(fp)

    def execute(self, query, data):

        self.cursor.execute(query, data)

    def commit(self):
        try:
            self.connection.commit()
        except Exception:
            self.connection.rollback()

    def insert_query(self, table_name):
        columns = self.tables[table_name]

        query = "INSERT INTO " + self.db_name + '.' + table_name + "\n"
        query += '(' + ','.join(columns) + ')\n'
        query += 'VALUES\n'
        # query += '(' + ",".join(data) + ')'
        query += '(' + ','.join(["%s"] * len(columns)) + ')'

        return query

    def on_dulpicate_key_update(self, colname, value):
        return "ON DUPLICATE KEY UPDATE {} = {};".format(colname, value)
