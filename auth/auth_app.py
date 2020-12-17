"""
ticket-system auth server
"""

import datetime
import re

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

from auth.db import account_exists
from auth.db import db_check
from auth.db import get_session_id
from auth.db import update_session_id
from auth.db import user_exists

app = Flask(__name__)


def main():
    db_check()
    app.run('0.0.0.0', port=8080)


@app.route('/auth/login/', methods=['POST'])
def login():
    """
    login view
    """
    username = password = ''
    if not isinstance(request.get_json(), dict):
        return "json required", 400
    else:
        json_parse = request.get_json()
        if 'username' in json_parse and 'password' in json_parse:
            username = json_parse["username"]
            password = json_parse["password"]

        if account_exists(username, password):
            session_id = create_session_id(username)
            return make_response(jsonify({'sessionid': session_id}), 200)

        return "Invalid username/password supplied", 400


@app.route('/auth/logout/', methods=['POST'])
def logout():
    """
    logout view
    """
    username = ''
    if not isinstance(request.get_json(), dict):
        return "json required", 400
    else:
        json_parse = request.get_json()
        if 'username' in json_parse:
            username = json_parse["username"]  # todo check for input

        if user_exists(username):
            if int(get_session_id(username)):
                update_session_id(username, '0')
                return 'successful', 200

            return "user unauthorized", 401

        return "Invalid username supplied", 400


def create_session_id(username: str):
    """
    Create session id function
    :param username: str
    :return: str
    """
    non_decimal = re.compile(r'[^\d]+')
    current_datetime = non_decimal.sub('', str(datetime.datetime.now()))[:20]
    update_session_id(username, current_datetime)
    return current_datetime


if __name__ == '__main__':
    main()
