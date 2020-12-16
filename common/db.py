"""
connector to postgresql db
"""

import os

import psycopg2
from dotenv import load_dotenv


class Connector:
    def __init__(self):
        load_dotenv()
        __host = os.getenv('PSQL_HOST')
        __port = os.getenv('PSQL_PORT')
        __db = os.getenv('PSQL_DB')
        __uid = os.getenv('PSQL_USERNAME')
        __pwd = os.getenv('PSQL_PWD')

        self.__connection = psycopg2.connect(dbname=__db, user=__uid, password=__pwd, host=__host, port=__port)
        self.__cursor = None

    def __enter__(self):
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.__connection.rollback()
            self.__cursor.close()
        else:
            self.__connection.commit()
            self.__cursor.close()



