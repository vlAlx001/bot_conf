# -*- coding: utf-8 -*-

from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    group = State()
    id = State()
    name = State()
    num = State()

class DelReg(StatesGroup):
    otvet = State()

class StartSend(StatesGroup):
    names = State()
    msg_temp = State()
    text = State()
    link = State()

class AnswerSend(StatesGroup):
    id_in = State()
    id_answer = State()
    names_in = State()
    names_answer = State()
    msg_temp = State()
    text = State()
    text_answer = State()

class StartSurvey(StatesGroup):
    names = State()
    text = State()
    msg_temp = State()


class Questions(StatesGroup):
    id = State()
    msg_text = State()
    text = State()

class Answer(StatesGroup):
    id = State()
    msg_text = State()
    text = State()
