# -*- coding: utf-8 -*-
import sqlite3
import helper


class DBWorker:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_name = "bikes.db"

    def execute_query(self, query):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        records = self.cursor.execute(query).fetchall()
        self.connection.commit()
        self.connection.close()
        return records

    def execute_and_return_json(self, query):
        records = self.execute_query(query)
        records_json = [dict(rec) for rec in records]
        return records_json

    def insert_into_login_data_table(self, login, password):
        query = "INSERT INTO login_data VALUES ('{0}', '{1}')".format(login, password)
        self.execute_query(query)

    def insert_into_users_data_table(self, login, fname, sname, age, city, email):
        query = "INSERT INTO users_data VALUES (NULL, '{0}', '{1}', '{2}', {3}, '{4}', '{5}',  '')".\
                format(login, fname, sname, age, city, email)
        self.execute_query(query)

    def confirm_login_data(self, login, password):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        query = "SELECT * FROM login_data WHERE login='{0}' AND password='{1}'".format(login, password)
        records = self.execute_query(query)
        return len(records) > 0

    def get_me_data(self, access_token):
        query = "SELECT client_id FROM access_data WHERE access_token='{0}'".format(access_token)
        records = self.execute_query(query)
        if len(records) == 1:
            client_id = records[0][0]
            login = self.get_login_by_client_id(client_id)
            query = "SELECT firstname, secondname FROM users_data WHERE login='{0}'".format(login)
            return self.execute_and_return_json(query)
        return ""

    def get_all_users(self, page):
        offset = (int(page)-1) * helper.records_per_page
        query = "SELECT firstname, secondname, age, city FROM users_data " \
                "LIMIT {0} OFFSET {1}".format(helper.records_per_page, offset)
        return self.execute_and_return_json(query)

    def get_user_by_id(self, _id):
        query = "SELECT firstname, secondname, age, city, email, " \
                "bikes FROM users_data WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_all_bikes(self, page):
        offset = (int(page)-1) * helper.records_per_page
        query = "SELECT firm, model, cost FROM bikes_data " \
                "LIMIT {0} OFFSET {1}".format(helper.records_per_page, offset)
        return self.execute_and_return_json(query)

    def get_bikes_by_id(self, _id):
        query = "SELECT firm, model, color, cost, description, " \
                "users FROM bikes_data WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def check_user_and_client_id(self, login, client_id):
        query = "SELECT client_id FROM app_data WHERE login='{0}' " \
                "AND client_id='{1}'".format(login, client_id)
        records = self.execute_query(query)
        return len(records) > 0

    def add_to_code_data(self, login, client_id, code, exp_time, redirect_uri):
        query = "INSERT INTO code_data VALUES ('{0}', '{1}', '{2}', {3}, " \
                "'{4}')".format(login, client_id, code, exp_time, redirect_uri)
        self.execute_query(query)

    def remove_from_code_data(self, login, client_id):
        query = "DELETE FROM code_data WHERE login='{0}' AND client_id='{1}'".format(login, client_id)
        self.execute_query(query)

    def get_login_by_client_id(self, client_id):
        query = "SELECT login FROM app_data WHERE client_id='{0}'".format(client_id)
        records = self.execute_query(query)
        if len(records) == 1:
            return records[0][0]
        return ""

    def check_code_for_getting_token(self, login, code, client_id, client_secret, uri):
        query = "SELECT client_secret FROM app_data WHERE client_id='{0}'".format(client_id)
        records = self.execute_query(query)
        if len(records) != 1:
            raise Exception("invalid client_id")
        db_secret = records[0][0]
        if db_secret != client_secret:
            raise Exception("invalid client_secret")
        query = "SELECT code, expiration_time, redirect_uri FROM code_data WHERE " \
                "login='{0}' AND client_id='{1}'".format(login, client_id)
        records = self.execute_query(query)
        if len(records) != 1:
            raise Exception("invalid login or client_id")
        db_code = records[0][0]
        if db_code != code:
            raise Exception("invalid code")
        db_uri = records[0][2]
        if db_uri != uri:
            raise Exception("invalid redirect_uri")
        db_time = records[0][1]
        if int(db_time) < int(helper.time()):
            raise Exception("timeout")

    def add_to_access_data(self, client_id, access_token, refresh_token, exp_time):
        query = "INSERT INTO access_data VALUES ('{0}', '{1}', '{2}', " \
                "'{3}')".format(client_id, access_token, refresh_token, exp_time)
        self.execute_query(query)

    def check_token(self, access_token):
        query = "SELECT expiration_time FROM access_data WHERE access_token='{0}'".format(access_token)
        records = self.execute_query(query)
        if len(records) != 1:
            raise Exception("invalid access_token")
        db_time = records[0][0]
        if int(db_time) < int(helper.time()):
            raise Exception("timeout")

    def check_for_refresh_token(self, client_id, client_secret, refresh_token):
        query = "SELECT client_secret FROM app_data WHERE client_id='{0}'".format(client_id)
        records = self.execute_query(query)
        if len(records) != 1:
            raise Exception("invalid client_id")
        db_secret = records[0][0]
        if db_secret != client_secret:
            raise Exception("invalid client_secret")
        query = "SELECT refresh_token FROM access_data WHERE client_id='{0}' " \
                "AND refresh_token='{1}'".format(client_id, refresh_token)
        records = self.execute_query(query)
        if len(records) != 1:
            raise Exception("invalid refresh_token")

    def update_access_data(self, client_id, refresh_token_old, access_token, refresh_token, exp_time):
        query = "UPDATE access_data SET access_token='{0}', " \
                "refresh_token='{1}', expiration_time={2} WHERE client_id='{3}' " \
                "AND refresh_token='{4}'".format(access_token, refresh_token, exp_time, client_id, refresh_token_old)
        self.execute_query(query)

    def get_count_records_in_table(self, table):
        query = "SELECT COUNT(*) FROM {0}".format(table)
        return self.execute_query(query)[0][0]
