import json
import random
import string
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

import config

login_user = {}


def verify(user, pwd):
    passwds = json.load(open(config.passwd_path, 'r'))
    if user in passwds and check_password_hash(passwds[user], pwd):
        return True
    return False


def login(response, user):
    login_str = ''.join(random.sample(string.ascii_letters + string.digits + '!@#$%^&*()', 16))
    if user not in login_user:
        login_user[user] = []
    login_user[user].insert(0, {'login_str': login_str, 'login_date': datetime.now()})
    response.set_cookie('user', user, expires = datetime.today() + timedelta(7))
    response.set_cookie('login_str', login_str, expires = datetime.today() + timedelta(7))


def verify_login_str(cookies, user):
    flag = False
    for i in range(len(login_user[user]) - 1, -1, -1):
        if (datetime.now() - login_user[user][i]['login_date']).days > 7:
            del login_user[user][i]
        elif cookies.get('login_str', None) == login_user[user][i]['login_str']:
            flag = True
    return flag


def verify_already_login(cookies):
    user = cookies.get('user', None)
    return user in login_user and verify_login_str(cookies, user)


if __name__ == '__main__':
    passwds = {}
    for passwd in passwds:
        passwds[passwd] = generate_password_hash(passwds[passwd])
    json.dump(passwds, open('config/user.db', 'w'))
    print(passwds)
