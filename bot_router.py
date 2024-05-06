# -*- coding: utf-8 -*-

import qrcode
import shutil

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link

from init import bot, bot_all_key, bot_dir
from router_state import Reg
from router_key import key_no, key_I, key_R
from router_init import get_reg, set_reg, del_reg


router = Router()

@router.message(F.text, Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if len(msg.text.split()) > 1:
        #to-do отработка алгоритма начального входа для участников
        await state.set_state(Reg.name)
        _, new_user = msg.text.split()
        if new_user == 'resp':
            #to-do
            await state.update_data(group='resp')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день! Я бот, буду помогать оперативно управлять конференцией\n' +
                                             'В мои обызанности входит своекреммно доводить до Вас информацию\n\n') +
                             'Представьтесь пожалуйста, как Вас будут видет другие участники конференции\n'+
                             'Ваше Имя Отчество Фамилия')
        elif new_user == 'analitic':
            #to-do
            await state.update_data(group='analitic')
            await state.update_data(id=msg.from_user.id)
            await msg.answer('Привет! Я бот. Я знаю, что ты Аналитик, что будем делать?')
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
        pass
    if user_reg == 'analitic':
        #to-do
        pass
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
    if user_reg == 'resp':
        #to-do
        
        return
    if user_reg == 'analitic':
        #to-do
        return
    global bot_all_key
    if hash(msg.text) == bot_all_key:
        set_reg(data['id'], data['group'])
        await msg.answer('Ваш статус подтверждён\n Вы Администратор Бота')
    else:
        await msg.answer('Вы не правильно ввели пароль!')
    await state.clear()
    


@router.message(Command('stop'))
async def stop_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if len(msg.text.split()) > 1 and user_reg == 'admin':
        _, new_user = msg.text.split()
        if new_user == 'del':
            shutil.rmtree('./data/')
            await msg.answer('Данные удалены полностью!\nБот завершил свою работу')
            exit()
        else:
            await msg.answer('Вы ошиблись с вводом данных')
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return




@router.message(Reg.num)
async def stop_2(msg: Message, state: FSMContext):
    await state.update_data(num=msg.text)
    data = await state.get_data()
    await msg.answer(f'Сохранил ответ {data["name"]} и {data["num"]}!!!!')
    await state.clear()


@router.message(Command('help'))
async def help_handler(msg: Message):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    #print(dir(msg))
    print(msg.from_user.id)
    print(msg.content_type)
    print(msg.date)
    print(msg.from_user)
    print(msg.message_id)
    print(msg.text)
    print('\n\n\n')
    a = await bot.get_me()
    #print(bot.get_me())
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
