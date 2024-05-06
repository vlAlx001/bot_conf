# -*- coding: utf-8 -*-

import os
import json
import logging
import requests
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# Задаётся папка для хранения временных файлов на случай сбоев
# !!! При пероначальном запуске проверьте папку на наличие старых файлов !!!
bot_dir = './data/'
if not(os.path.isdir(bot_dir)): os.mkdir(bot_dir)

logging.basicConfig(level=logging.DEBUG, filename=f'{bot_dir}bot_log.log', \
    format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")
'''
Логирование
filemode="w" - каждый раз перезаписывает журнал
filemode="a" - добавление записей в журнал
'''
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# команды для бота
'''
start - Активность
stop - Выйти из конференции
help - Помощь
'''

# Записать пароль Администратора (для противодействия захвата бота)
# Администратором может быть только один зарегистрированный аккаунт
# Для регистрации или смены Администратора используйте комманду '/start admin'
bot_all_key = hash(os.getenv('KEY'))

load_user = {
    'admin': 0,
    'analitic': [],
    'resp': []
}

def main():
    global load_user
    if os.path.isfile(f'{bot_dir}/user.json'):
        with open(f'{bot_dir}/user.json', 'r') as f:
            load_user = json.load(f)
    else:
        with open(f'{bot_dir}user.json', 'w') as f:
            json.dump(load_user, f)
    try:
        url = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/getMe'
        if requests.get(url).status_code != 200: raise Exception('Бот не отвечает!')
    except Exception as e:
        logging.error('Недействительный токен бота', exc_info=True)
        exit()

if __name__ != '__main__':
    main()
