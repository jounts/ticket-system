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
                   f"{conf.AUTH_F_SID} varchar(10) NOT NULL," \
                   f"{conf.AUTH_F_SKILL} integer NOT NULL," \
                   f"PRIMARY KEY ({conf.AUTH_F_USERNAME}))"
        cursor.execute(exec_msg)


def insert_test_user(conn: Connector) -> None:
    """
    Insert test user into db function
    :param conn: Connection object
    :return: None
    """
    if user_exists(conf.NAME, conn):
        with conn as cursor:
            exec_msg = f"INSERT INTO {conf.AUTH_TABLE_NAME}" \
                       f"({conf.AUTH_F_USERNAME}, {conf.AUTH_F_PASSWORD}, {conf.AUTH_F_SID}, {conf.AUTH_F_SKILL}) " \
                       f"VALUES (%s, %s, %s, %s)"
            cursor.execute(exec_msg, (conf.NAME, conf.PASSWORD, '-1', conf.SKILL))


def user_exists(username: str, conn: Connector) -> bool:
    """
    Existing username in db function
    :param username: str
    :param conn: Connection object
    :return:
    """
    with conn as cursor:
        exec_msg = f"SELECT username FROM {conf.AUTH_TABLE_NAME} where username = '{username}'"
        cursor.execute(exec_msg)
        exec_response = list(itertools.chain(*cursor.fetchall()))
        if exec_response == username:
            return True

        return False


if __name__ == '__main__':
    db_check()
