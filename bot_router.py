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
from router_state import Reg, DelReg, StartSend, StartSurvey, Questions
from router_key import key_no, key_I, key_R
from router_init import get_list_id, get_reg, set_reg, del_reg
from router_init import get_user, set_user, del_user
from router_init import set_questions, get_questions

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
                             'Фамилия Имя Отчество')
        elif new_user == 'analitic':
            await state.update_data(group='analitic')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день! Я бот, буду помогать оперативно управлять конференцией.\n' +
                                             'В мои обязанности входит своевременно доводить информацию') +
                             'Представьтесь, пожалуйста.\n'+
                             'Фамилия Имя Отчество')
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
        key = [
            {
                'Задать вопрос': 'question_text',
                'Поднять руку': 'hand'
            }
        ]
        await msg.answer('Подскажите, что Вам нужно', reply_markup=await key_I(key))
    if user_reg == 'analitic':
        #to-do
        temp_questions = get_questions()
        if len(temp_questions) == 0:
            key = []
        else:
            key = [{'Список вопросов': 'question_list'}]
        key.append({'Создать рассылку': 'send', 'Создать опрос': 'survey'})
        key.append({'Отмена': 'cancle'})
        await msg.answer(html.bold('Выберите действие'), reply_markup=await key_I(key))
        
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
        await msg.answer(f'Вас зовут: {html.bold(msg.text)}\n', 
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

@router.callback_query(F.data == 'hand')
async def start_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    list_temp = get_list_id('analitic')
    names = get_user(call.from_user.id)
    for i in list_temp:
        i = int(i)
        await bot.send_message(chat_id=i, text=f'Поступил запрос выступить {names[0]}')
    await call.message.answer('Ваш запрос выступить отправлен Аналитикам')

@router.callback_query(F.data == 'question_list')
async def start_send(call: CallbackQuery, state: FSMContext):
    #to-do
    await call.answer()
    temp_questions = get_questions()
    await call.message.delete()
    await call.message.answer(f'Имеются вопросы в кол-ве {len(temp_questions)} шт.\n'+
                              'Функция ещё будет дописываться')

@router.callback_query(F.data == 'send')
async def start_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.text)    
    await state.update_data(names = get_user(call.from_user.id)[0])
    await state.update_data(msg_temp = call.message.message_id)
    await call.message.edit_text('ВВедите текст сообшения')

@router.message(StartSend.text)
async def start_send_1(msg: Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(msg.chat.id, data['msg_temp'])
    await bot.delete_message(msg.chat.id, data['msg_temp']+1)
    await state.update_data(text = msg.text)
    key = [
            {
                'Отправить': 'msg_send'
            }, 
            {
                'Изменить текст': 'text_edit'
            },
            {
                'Добавить ссылку': 'link'
            }, 
            {
                'Отмена': 'cancle'
            }
        ]
    msg_tsxt = html.bold('Проверьте Ваше сообшение перед отправкой:\n\n')
    msg_tsxt += f'Сообщение отправил аналитик {data["names"]}:\n'
    msg_tsxt += f'{html.blockquote(msg.text)}'
    if data.get('link', False):
        msg_tsxt += f'{hide_link(data["link"])}'
    await msg.answer(msg_tsxt, reply_markup=await key_I(key))

@router.callback_query(F.data == 'msg_send')
async def start_send(call: CallbackQuery, state: FSMContext):
    #to-do
    await call.answer()
    data = await state.get_data()
    list_resp = get_list_id()
    msg_text = f'Сообщение отправил аналитик {data["names"]}:\n'
    msg_text += f'{html.blockquote(data["text"])}'
    if data.get('link', False):
        msg_text += f'{hide_link(data["link"])}'
    key = [
            {
                'У меня есть вопрос': 'question_text'
            }
        ]
    for i in list_resp:
        i = int(i)
        await bot.send_message(chat_id=i, text=msg_text, reply_markup= await key_I(key))
    await state.clear()

@router.callback_query(F.data == 'text_edit')
async def start_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.text)
    await state.update_data(msg_temp = call.message.message_id)
    data = await state.get_data()
    await call.message.edit_text('Текст Вашего сообщения:\n'
                                 f'{data["text"]}\n\n'
                                 +'Введите текст сообшения')

@router.callback_query(F.data == 'link')
async def start_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.link)
    await state.update_data(msg_temp = call.message.message_id)
    data = await state.get_data()
    await call.message.edit_text('Текст Вашего сообщения:\n'
                                 f'{data["text"]}\n\n'
                                 +'Введите ссылку для добавления в сообшение')

@router.message(StartSend.link)
async def start_send_1(msg: Message, state: FSMContext):
    await state.update_data(link = msg.text)
    data = await state.get_data()
    await bot.delete_message(msg.chat.id, data['msg_temp'])
    await bot.delete_message(msg.chat.id, data['msg_temp']+1)
    key = [
            {
                'Отправить': 'msg_send'
            }, 
            {
                'Изменить текст': 'text_edit'
            },
            {
                'Добавить ссылку': 'link'
            }, 
            {
                'Отмена': 'cancle'
            }
        ]
    msg_text = html.bold('Проверьте Ваше сообшение перед отправкой:\n\n')
    msg_text += f'Сообщение отправил аналитик {data["names"]}:\n'
    msg_text += f'{html.blockquote(data["text"])}'
    if data.get('link', False):
        msg_text += f'{hide_link(data["link"])}'
    await msg.answer(msg_text, reply_markup=await key_I(key))

@router.callback_query(F.data == 'question_text')
async def start_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Questions.text)
    await state.update_data(id = call.from_user.id)
    await state.update_data(msg_text = call.message.text)
    await call.message.answer('Опишите свой вопрос и мы Вам ответим, как можно скорее')

@router.message(Questions.text)
async def start_send_1(msg: Message, state: FSMContext):
    await state.set_state(Questions.text)
    await state.update_data(text = msg.text)
    data = await state.get_data()
    if set_questions(data):
        list_temp = get_list_id('analitic')
        names = get_user(msg.from_user.id)
        for i in list_temp:
            i = int(i)
            await bot.send_message(chat_id=i, text=f'Поступил вопрос от {names[0]}')
        await msg.answer('Ваш вопрос направлен Аналитикам')
    else:
        await msg.answer('Ваш вопрос был потерян!\n'+
                         'Обратитесь пожалуйста к администратору!')

@router.callback_query(F.data == 'survey')
async def start_survey(call: CallbackQuery, state: FSMContext):
    #to-do
    await call.answer()
    await call.message.delete()
    await call.message.answer('Функция ещё в разработке!')

@router.callback_query(F.data == 'cancle')
async def cancle(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.clear()

@router.message(Command('stop'))
async def stop_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    
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
    await msg.answer(html.blockquote('ЭТА ФУНКЦИЯ ЕЩЁ В РАЗРАБОТКЕ!!!\nВсе данные для примера оформления текста')) # 
    print(msg.from_user.id)
    print(msg.content_type)
    print(msg.date)
    print(msg.from_user)
    print(msg.message_id)
    print(msg.text)
    a = await bot.get_me()
    print(a.username)
    get_user(msg.from_user.id)
    await msg.answer(f"Твои данные в базе: {get_user(msg.from_user.id)}") # 
    await msg.answer(f"Твой простой ID: {msg.from_user.id}") # 
    await msg.answer(f"Твой жирный ID: {html.bold(msg.from_user.id)}") # 
    await msg.answer(f"Твой курсив ID: {html.italic(msg.from_user.id)}") # 
    await msg.answer(f"Твой блок ID: {html.blockquote(msg.from_user.id)}") # 
    await msg.answer(f"Твой код ID: {html.code(msg.from_user.id)}") # 
    await msg.answer(f"Твой зачеркнутый ID: {html.underline(msg.from_user.id)}") # 
    await msg.answer(f'Прикольно же\n {hide_link("https://telegra.ph/Konfa-05-04")}\n'+\
                     'Очень прикольно!!!') # 

@router.message(F.text)
async def message_handler(msg: Message):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    await msg.answer('Функция ещё в разработке!')
    