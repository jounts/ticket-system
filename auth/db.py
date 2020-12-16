"""
db check and prepare
"""

import itertools

from common.db import Connector
from common import conf


def db_check() -> None:
    """
    DB check and prepare for auth app function
    :return: None
    """
    conn = Connector()

    with conn as cursor:
        cursor.execute(f"SELECT table_name "
                       f"FROM information_schema.tables "
                       f"WHERE table_schema = 'public' "
                       f"ORDER BY table_name")

        exec_response = list(itertools.chain(*cursor.fetchall()))

        if conf.AUTH_TABLE_NAME not in exec_response:
            db_prepare(conn)

        if conf.TEST_KEY:
            insert_test_user(conn)


def db_prepare(conn: Connector) -> None:
    """
    Prepare DB for auth app function
    :param conn: Connection object
    :return: None
    """
    with conn as cursor:
        exec_msg = "CREATE TABLE auth_user(" \
                   f"{conf.AUTH_F_USERNAME} varchar(50) NOT NULL," \
                   f"{conf.AUTH_F_PASSWORD} varchar(250) NOT NULL," \
                   f"{conf.AUTH_F_SID} varchar(20) NOT NULL," \
                   f"{conf.AUTH_F_SKILL} integer NOT NULL," \
                   f"PRIMARY KEY ({conf.AUTH_F_USERNAME}))"
        cursor.execute(exec_msg)


def insert_test_user(conn: Connector) -> None:
    """
    Insert test user into db function
    :param conn: Connection object
    :return: None
    """
    if not user_exists(conf.NAME):
        with conn as cursor:
            exec_msg = f"INSERT INTO {conf.AUTH_TABLE_NAME}" \
                       f"({conf.AUTH_F_USERNAME}, {conf.AUTH_F_PASSWORD}, {conf.AUTH_F_SID}, {conf.AUTH_F_SKILL}) " \
                       f"VALUES (%s, %s, %s, %s)"
            cursor.execute(exec_msg, (conf.NAME, conf.PASSWORD, '-1', conf.SKILL))


def user_exists(username: str) -> bool:
    """
    Existing username in db function
    :param username: str
    :return: bool
    """
    conn = Connector()
    with conn as cursor:
        exec_msg = f"SELECT {conf.AUTH_F_USERNAME} FROM {conf.AUTH_TABLE_NAME} where username = %s"
        cursor.execute(exec_msg, (username,))
        return cursor.fetchone() is not None


def account_exists(username: str, password: str) -> bool:
    """
    Existing account in db function
    :param username: str
    :param password: str
    :return: bool
    """
    conn = Connector()
    with conn as cursor:
        exec_msg = f"select {conf.AUTH_F_USERNAME} " \
                   f"from {conf.AUTH_TABLE_NAME} " \
                   f"where {conf.AUTH_F_USERNAME} = %s and {conf.AUTH_F_PASSWORD} = %s"
        cursor.execute(exec_msg, (username, password))
        return cursor.fetchone() is not None


if __name__ == '__main__':
    db_check()
