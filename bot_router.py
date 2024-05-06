# -*- coding: utf-8 -*-

import qrcode
import shutil

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from init import bot, bot_all_key, bot_dir, logging
from router_state import Reg, DelReg
from router_key import key_no, key_I, key_R
from router_init import get_reg, set_reg, del_reg, get_user, set_user, del_user


router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if len(msg.text.split()) > 1:
        #to-do отработка алгоритма начального входа для участников
        if user_reg == 'resp': 
            await msg.answer(html.bold('Вы уже зарегистрированы Участником конференции\n'+
                                       'Если Вы ошибочно зарегистрировались удалите регистрацию через команду /stop'))
            return
        if user_reg == 'analitic': 
            await msg.answer(html.bold('Вы уже зарегистрированы Аналитиком конференции\n'+
                                       'Если Вы ошибочно зарегистрировались удалите регистрацию через команду /stop'))
            return
        await state.set_state(Reg.name)
        _, new_user = msg.text.split()
        if new_user == 'resp':
            await state.update_data(group='resp')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день! Я бот, буду помогать оперативно управлять конференцией.\n' +
                                             'В мои обязанности входит своевременно доводить информацию') +
                             'Представьтесь, пожалуйста.\n'+
                             'Имя Отчество Фамилия')
        elif new_user == 'analitic':
            await state.update_data(group='analitic')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день! Я бот, буду помогать оперативно управлять конференцией.\n' +
                                             'В мои обязанности входит своевременно доводить информацию') +
                             'Представьтесь, пожалуйста.\n'+
                             'Имя Отчество Фамилия')
        elif new_user == 'admin':
            await state.update_data(group='admin')
            await state.update_data(id=msg.from_user.id)
            await msg.answer('Вы пытаетесь изменить Администратора Бота\n'+
                             'Подтвердите свои права доступа!\nВведите пароль')
        else:
            await msg.answer('Вы ошиблись с вводом данных')
        return
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    if user_reg == 'resp':
        #to-do
        await msg.answer('Функция ещё в разработке!')
    if user_reg == 'analitic':
        #to-do
        await msg.answer('Функция ещё в разработке!')
    if user_reg == 'admin':
        a = await bot.get_me()
        a = a.username
        data = f'https://t.me/{a}?start=analitic'
        img = qrcode.make(data)
        img.save(f'{bot_dir}qr-code analitic.png')
        img = FSInputFile(f'{bot_dir}qr-code analitic.png')
        await msg.answer('QR-код для аналитиков')
        await msg.answer_photo(photo=img, caption=data)
        data = f'https://t.me/{a}?start=resp'
        img = qrcode.make(data)
        img.save(f'{bot_dir}qr-code resp.png')
        img = FSInputFile(f'{bot_dir}qr-code resp.png')
        await msg.answer('QR-код для респондентов')
        await msg.answer_photo(photo=img, caption=data)

@router.message(Reg.name)
async def start_reg_1(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_reg = data['group']
    if user_reg == 'resp' or user_reg == 'analitic':
        await state.set_state(Reg.num)
        await state.update_data(name=msg.text)
        key = [['Парвильно', 'Изменить']]
        await msg.answer(f'Вас зовут {html.bold(msg.text)}\n', 
                         reply_markup=await key_R(key, 'Всё правильно проверьте?'))
        return
    else:
        global bot_all_key
        if hash(msg.text) == bot_all_key:
            set_reg(data['id'], data['group'])
            await msg.answer('Ваш статус подтверждён\n Вы Администратор Бота')
        else:
            await msg.answer('Вы не правильно ввели пароль!')
        await state.clear()
    
@router.message(Reg.num)
async def start_reg_2(msg: Message, state: FSMContext):
    if msg.text == 'Парвильно':
        key = [['Отказаться', 'Ввести номер телефона']]
        await msg.answer(f'По желанию Вы можете поделиться Вашим номером телефона для связи', 
                         reply_markup=await key_R(key, 'Вы желаете поделиться номером телефона?'))
        return
    elif msg.text == 'Изменить':
        await state.set_state(Reg.name)
        await msg.answer('Представьтесь пожалуйста, как Вас будут видет другие участники конференции\n'+
                         'Ваше Имя Отчество Фамилия')
        return
    elif msg.text == 'Отказаться':
        pass
    elif msg.text == 'Ввести номер телефона':
        return
    else:
        await state.update_data(num=msg.text)
    data = await state.get_data()
    await msg.answer('Благодарю за регистрацию', reply_markup=key_no())
    set_reg(data['id'], data['group'])
    set_user(data)
    await state.clear()


@router.message(Command('stop'))
async def stop_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    #to-do расписть удаление участников
    if len(msg.text.split()) > 1 and user_reg == 'admin':
        _, new_user = msg.text.split()
        if new_user == 'del':
            shutil.rmtree('./data/')
            await msg.answer('Данные удалены полностью!\nБот завершил свою работу')
            exit()
        else:
            await msg.answer('Вы ошиблись с вводом данных')
    if user_reg == 'admin':
        await msg.answer('Функция пока не дописана!')
        return
    await state.set_state(DelReg.otvet)
    key = [['ДА, точно', 'НЕТ, это ошибка']]
    await msg.answer('Вы правда хотите удалить свои данные из конференции?', 
                     reply_markup=await key_R(key, 'Вы уверены?'))


@router.message(DelReg.otvet)
async def stop_handler_1(msg: Message, state: FSMContext):
    if msg.text == 'НЕТ, это ошибка':
        await msg.answer('Хорошо, я понял', reply_markup=key_no())
        await state.clear()
    elif msg.text == 'ДА, точно':
        A = del_reg(msg.from_user.id)
        B = del_user(msg.from_user.id) 
        if A and B:
            await msg.answer('Ваша данные удалены из коференции!', reply_markup=key_no())
        else:
            await msg.answer('Ваша данные удалены не полностью!\n'+
                             'Обратитесь пожалуйста к администратору!', reply_markup=key_no())
        await state.clear()
    else:
        await msg.answer('Вы ошиблись с вводом данных', reply_markup=key_no())
        await state.clear()


@router.message(Command('help'))
async def help_handler(msg: Message):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    print(msg.from_user.id)
    print(msg.content_type)
    print(msg.date)
    print(msg.from_user)
    print(msg.message_id)
    print(msg.text)
    a = await bot.get_me()
    print(a.username)
    await msg.answer(f"Твой простой ID: {msg.from_user.id}") # 
    await msg.answer(f"Твой жирный ID: {html.bold(msg.from_user.id)}") # 
    await msg.answer(f"Твой курсив ID: {html.italic(msg.from_user.id)}") # 
    await msg.answer(f"Твой блок ID: {html.blockquote(msg.from_user.id)}") # 
    await msg.answer(f"Твой код ID: {html.code(msg.from_user.id)}") # 
    await msg.answer(f"Твой зачеркнутый ID: {html.underline(msg.from_user.id)}") # 
    key = [['Изменить настройки', 'Показать попу (_!_)'], ['new']]
    await msg.answer(f'Твой курсив ID: {html.italic(msg.from_user.id)}', reply_markup=await key_R(key, 'Что хотел?')) # 


@router.message(F.text)
async def message_handler(msg: Message):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    await msg.answer(f"Твой простой ID: {msg.from_user.id}") # 
    await msg.answer(f"Твой жирный ID: {html.bold(msg.from_user.id)}") # 
    await msg.answer(f"Твой курсив ID: {html.italic(msg.from_user.id)}") # 
    await msg.answer(f"Твой блок ID: {html.blockquote(msg.from_user.id)}") # 
    await msg.answer(f"Твой код ID: {html.code(msg.from_user.id)}") # 
    await msg.answer(f"Твой зачеркнутый ID: {html.underline(msg.from_user.id)}") # 
    await msg.answer(f'Прикольно же\n {hide_link("https://telegra.ph/Konfa-05-04")}\n'+\
                     'Очень прикольно!!!') # 
    key = [
        {
            'Да': 'join',
            'no': 'jop'
        }, 
        {
            'Нет': 'cancle'
        }
    ]
    await msg.answer(f"Твой блок ID: {html.blockquote(msg.from_user.id)}",
                     reply_markup=await key_I(key)) # 



@router.callback_query(F.data == 'join')
async def join(call: CallbackQuery):
   await call.answer()
   await call.message.answer('УГУ')


@router.callback_query(F.data == 'cancle')
async def cancle(call: CallbackQuery):
   await call.answer()
   await call.message.answer('Ты вернулся В главное меню.')
