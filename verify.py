import time
import hashlib


def md5(text):
    '''md5 encrypto'''

    _m = hashlib.md5()
    _m.update(text)
    return _m.hexdigest()


# def get_global_code(salt = "pwd"):
#     ''' get time code'''
#
#     _time = time.localtime()
#     return "{}{}{}".format(_time[0], _time[1], _time[2]) + salt


def verify(pwd):
    passwds = ['35c1b91be35222bc7ed93a64b61830b9', '2083ab175ac97f1a1ad8eea3063f24dc']
    for passwd in passwds:
        if passwd == md5(pwd.encode()):
            return True
    return False


if __name__ == '__main__':
    passwds = []
    encode_passwds = []
    for passwd in passwds:
        encode_passwds.append(md5(passwd.encode()))
    print(encode_passwds)
