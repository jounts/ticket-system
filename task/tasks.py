"""
db check and prepare
"""

import itertools
import os

from common.db import Connector
import conf


def db_check() -> None:
    """
    DB check and prepare for TASK app function
    :return: None
    """
    conn = Connector()

    print(os.getenv('PSQL_HOST'))

    with conn as cursor:
        cursor.execute(f"SELECT table_name "
                       f"FROM information_schema.tables "
                       f"WHERE table_schema = 'public' "
                       f"ORDER BY table_name")

        exec_response = list(itertools.chain(*cursor.fetchall()))

        if conf.TASK_TABLE_NAME not in exec_response:
            db_prepare(conn)

        if conf.TEST_KEY:
            insert_test_task(conn)


def db_prepare(conn: Connector) -> None:
    """
    Prepare DB for TASK app function
    :param conn: Connection object
    :return: None
    """
    with conn as cursor:
        exec_msg = "CREATE TABLE tasks(" \
                   f"{conf.TASK_F_NAME} char(50) PRIMARY KEY NOT NULL," \
                   f"{conf.TASK_F_STATUS} state NOT NULL," \
                   f"{conf.TASK_F_LEVEL} integer NOT NULL," \
                   f"{conf.TASK_F_USER} char(50))"

        cursor.execute(exec_msg)


def insert_test_task(conn: Connector) -> None:
    """
    Insert test user into db function
    :param conn: Connection object
    :return: None
    """
    if not task_exists(conf.NAME):
        with conn as cursor:
            exec_msg = f"INSERT INTO {conf.TASK_TABLE_NAME}" \
                       f"({conf.TASK_F_NAME}, {conf.TASK_F_LEVEL}, {conf.TASK_F_USER}, {conf.TASK_F_STATUS}) " \
                       f"VALUES (%s, %s, %s, %s)"
            cursor.execute(exec_msg, (conf.NAME, conf.LEVEL, conf.USER, conf.STATUS))


def get_task_execs(name: str) -> tuple:
    conn = Connector()
    with conn as cursor:
        exec_msg = f"SELECT {conf.AUTH_F_USERNAME} " \
                   f"FROM {conf.AUTH_TABLE_NAME} " \
                   f"WHERE {conf.AUTH_F_SKILL} > (" \
                   f"SELECT {conf.TASK_F_LEVEL} " \
                   f"FROM {conf.TASK_TABLE_NAME} " \
                   f"WHERE {conf.TASK_F_NAME} = %s)"
        cursor.execute(exec_msg, (name,))
        exec_response = cursor.fetchall()
        return exec_response


def task_exists(name: str) -> bool:
    """
    Existing task in db function
    :param name: str
    :return: bool
    """
    conn = Connector()
    with conn as cursor:
        exec_msg = f"SELECT {conf.TASK_F_NAME} FROM {conf.TASK_TABLE_NAME} where name = %s"
        cursor.execute(exec_msg, (name,))
        return cursor.fetchone() is not None


if __name__ == '__main__':
    db_check()
