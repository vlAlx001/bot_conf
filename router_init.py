# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
from datetime import datetime

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
    temp_dict = {hash(data['text'].strip()): [str(data['id']), data['msg_text'], data['text']]}
    questions_list['id'].append(temp_dict)
    print(f'Кол-во вопросов: {len(questions_list["id"])}')
    save_json(questions_list, 'questions.json')
    return True

def get_questions() -> list:
    global questions_list
    return questions_list['id']

def get_answer(text: str) -> list:
    global questions_list
    for i in questions_list['id']:
        answer = i.get(hash(text.strip()))
        if answer: return answer
    logging.error('Непредвиденная работа функции get_answer, ответ не найден в базе!!!')
    return 

def del_answer(text:str) -> None:
    global questions_list
    a = ''
    b = []
    for i in questions_list['id']:
        answer = i.get(hash(text.strip()))
        if answer: continue
        b.append(i)
    questions_list['id'] = b
    save_json(questions_list, 'questions.json')

def load_answer():
    df = pd.DataFrame(columns=['datetime', 'name', 'names_answer', 
                               'msg_temp', 'text', 'text_answer'])
    if os.path.isfile('answer.xlsx'):
        df = pd.read_excel('answer.xlsx')
    df1 = df[['datetime', 'name', 'names_answer', 
                               'msg_temp', 'text', 'text_answer']].copy()
    return df1

def save_ansver(A: dict) -> None:
    df = load_answer()
    temp_dict = {
        'datetime': [str(datetime.now())],
        'name': [A['names_in']],
        'names_answer': [A['names_answer']],
        'msg_temp': [A['msg_temp']],
        'text': [A['text']],
        'text_answer': [A['text_answer']]
    }
    df1 = pd.DataFrame(temp_dict)
    df = pd.concat([df, df1])
    df.reset_index(drop=True).to_excel('answer.xlsx')
