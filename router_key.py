# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def key_no():
    return ReplyKeyboardRemove()

async def key_R(key, A=None):
    markup = []
    for i in key:
        markup.append([KeyboardButton(text=j) for j in i])
    markup = ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True, input_field_placeholder=A)
    return markup

async def key_I(key):
    markup = []
    for i in key:
        markup.append(InlineKeyboardButton(text=k, callback_data=v) for k, v in i.items())
    markup = InlineKeyboardMarkup(inline_keyboard=markup)
    return markup
