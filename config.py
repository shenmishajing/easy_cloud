'''
config module
this script will read base config and save to a Dict Object
'''

import os
import json

project_path = os.path.abspath(os.path.dirname(__file__)) + '/'
config_path = project_path + "config/baseconfig.cfg"
passwd_path = project_path + "config/user.db"
ssl_path = '/home/zwh/ssl-certificate/'
pem_path = ssl_path + '2882671_www.shenmishajing.tk.pem'
key_path = ssl_path + '2882671_www.shenmishajing.tk.key'

with open(config_path, "r", encoding = 'utf-8') as f:
    config = json.load(f)
