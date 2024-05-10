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
    foto = State()
    files = State()
    link = State()


class StartSurvey(StatesGroup):
    names = State()
    id = State()
    name = State()
    num = State()


class Questions(StatesGroup):
    id = State()
    msg_text = State()
    text = State()
