# -*- coding: utf-8 -*-

import json

from init import logging, load_user, id_user, bot_dir

def save_json(A: dict, file: str) -> bool:
    try:
        global bot_dir
        with open(f'{bot_dir}{file}', 'w') as f:
            json.dump(A, f)
        return True
    except Exception as e:
        logging.error(f'Файл {file} был заблокмрован', exc_info=True)
        return False

def get_reg(A: int) -> str | bool:
    global load_user
    if A in load_user['resp']: return 'resp'
    if A in load_user['analitic']: return 'analitic'
    if load_user['admin'] == A: return 'admin'
    return False

def set_reg(A: int, status) -> None:
    global load_user
    if status == 'admin':
        load_user[status] = A
    else:
        B = load_user[status]
        B.append(A)
        load_user[status] = B
    save_json(load_user, 'user.json')

def del_reg(A: int) -> bool:
    global load_user
    temp = get_reg(A)
    for i in range(len(load_user[temp])):
        if load_user[temp][i] == A:
            del load_user[temp][i]
    return save_json(load_user, 'user.json')

def get_user(A: int) -> dict:
    return

def set_user(A: dict) -> None:
    global id_user
    id_user[A['id']] = [A['name'], A.get('num', 0)]
    save_json(id_user, 'id_user.json')

def del_user(A: int) -> bool:
    global id_user
    del id_user[A]
    return save_json(id_user, 'id_user.json')