# -*- coding: utf-8 -*-

import json
import os

from init import logging, load_user, id_user, questions_list, bot_dir

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
    A = str(A)
    if A in load_user['resp']: return 'resp'
    if A in load_user['analitic']: return 'analitic'
    if load_user['admin'] == A: return 'admin'
    return False

def set_reg(A: int, status) -> None:
    global load_user
    A = str(A)
    if status == 'admin':
        load_user[status] = A
    else:
        B = load_user[status]
        B.append(A)
        load_user[status] = B
    save_json(load_user, 'user.json')

def del_reg(A: int) -> bool:
    global load_user
    A = str(A)
    temp = get_reg(A)
    for i in range(len(load_user[temp])):
        if load_user[temp][i] == A:
            del load_user[temp][i]
    return save_json(load_user, 'user.json')

def get_user(A: int) -> list | bool:
    global id_user
    A = str(A)
    if id_user.get(A, False) == False: 
        logging.error('Непредвиденная работа функции get_user!!!')
    return id_user.get(str(A), False)

def set_user(A: dict) -> None:
    global id_user
    id_user[str(A['id'])] = [A['name'], A.get('num', 0)]
    save_json(id_user, 'id_user.json')

def del_user(A: int) -> bool:
    global id_user
    A = str(A)
    del id_user[A]
    return save_json(id_user, 'id_user.json')

def get_list_id(A='resp') -> list:
    global load_user
    return load_user[A]

def set_questions(data: dict) -> bool:
    global questions_list
    print(questions_list)
    print(data)
    temp_dict = {str(data['id']): [data['msg_text'], data['text']]}
    questions_list['id'].append(temp_dict)
    print(questions_list)
    save_json(questions_list, 'questions.json')
    return True

def get_questions() -> list:
    global questions_list

    print(questions_list)

    return questions_list['id']