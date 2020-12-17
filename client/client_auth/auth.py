from requests import request

from .. import conf


def login(username: str, password: str) -> tuple:
    """
    login view
    :param username: str
    :param password: str
    :return: tuple(bool, str)
    """
    url = conf.AUTH_SERVER + conf.LOGIN_PATH
    method = 'POST'
    json = {
        conf.USERNAME_F: username,
        conf.PASSWORD_F: password
    }
    response = request(url=url, method=method, json=json)
    if response.status_code == conf.OK_STATUS:
        try:
            response_dict: dict = response.json()
            return True, response_dict[conf.SID_F]
        except ValueError:
            return False, 'wrong answer, try again'
    if response.status_code == conf.BAD_RQ_STATUS or response.status_code == conf.UN_AUTH_STATUS:
        return False, response.text


if __name__ == '__main__':
    pass
