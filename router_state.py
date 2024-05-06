# -*- coding: utf-8 -*-

from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    group = State()
    id = State()
    name = State()
    num = State()

class DelReg(StatesGroup):
    otvet = State()
