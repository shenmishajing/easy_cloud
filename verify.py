import json
from werkzeug.security import generate_password_hash, check_password_hash


def verify(user, pwd):
    passwds = json.load(open('config/user.db', 'r'))
    if user in passwds and check_password_hash(passwds[user], pwd):
        return True
    return False


if __name__ == '__main__':
    passwds = {}
    for passwd in passwds:
        passwds[passwd] = generate_password_hash(passwds[passwd])
    json.dump(passwds, open('config/user.db', 'w'))
    print(passwds)
