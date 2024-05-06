# -*- coding: utf-8 -*-

import json

from init import load_user, bot_dir, logging


def get_reg(A: int) -> str | bool:
    global load_user
    if A in load_user['resp']: return 'resp'
    if A in load_user['analitic']: return 'analitic'
    if load_user['admin'] == A: return 'admin'
    return False

def set_reg(A: int, status):
    global load_user
    if status == 'admin':
        load_user[status] = A
    else:
        B = load_user[status]
        B.append(A)
        load_user[status] = B
    try:
        with open(f'{bot_dir}user.json', 'w') as f:
            json.dump(load_user, f)
    except Exception as e:
        logging.error('Файл user.json был заблокмрован', exc_info=True)

def del_reg(A: int, status):
    pass