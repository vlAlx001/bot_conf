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
from router_state import Reg, DelReg, StartSend, StartSurvey, Questions, AnswerSend, Answer
from router_key import key_no, key_I, key_R
from router_init import get_list_id, get_reg, set_reg, del_reg
from router_init import get_user, set_user, del_user
from router_init import set_questions, get_questions
from router_init import get_answer, del_answer, save_ansver


router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if len(msg.text.split()) > 1:
        if user_reg == 'resp': 
            await msg.answer(html.bold('Вы уже зарегистрированы Дорогим гостем конференции\n'+
                                       'Если Вы ошибочно зарегистрировались удалите регистрацию через команду /stop'))
            return
        if user_reg == 'analitic': 
            await msg.answer(html.bold('Вы уже зарегистрированы Организатором конференции\n'+
                                       'Если Вы ошибочно зарегистрировались удалите регистрацию через команду /stop'))
            return
        await state.set_state(Reg.name)
        _, new_user = msg.text.split()
        if new_user == 'resp':
            await state.update_data(group='resp')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день, Дорогой гость конференции! Я бот, буду помогать оперативно управлять конференцией.\n' +
                                             'В мои обязанности входит своевременно доводить информацию') +
                             'Представьтесь, пожалуйста.\n'+
                             'Фамилия Имя Отчество')
        elif new_user == 'analitic':
            await state.update_data(group='analitic')
            await state.update_data(id=msg.from_user.id)
            await msg.answer(html.blockquote('Добрый день, Организатор! Я бот, буду помогать оперативно управлять конференцией.\n' +
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
        key = [
            {
                'Задать вопрос': 'question_text',
            },
            {
                'Отмена': 'cancle'
            }
        ]
        await msg.answer('Подскажите, Дорогой гость! Какой у Вас возник вопрос?', reply_markup=await key_I(key))
    if user_reg == 'analitic':
        #to-do добавить перечисление вопросов
        temp_questions = get_questions()
        if len(temp_questions) == 0:
            key = []
        else:
            key = [{'Список вопросов': 'question_list'}]
        key = []
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
        await msg.answer('QR-код для Организаторов')
        await msg.answer_photo(photo=img, caption=data)
        data = f'https://t.me/{a}?start=resp'
        img = qrcode.make(data)
        img.save(f'{bot_dir}qr-code resp.png')
        img = FSInputFile(f'{bot_dir}qr-code resp.png')
        await msg.answer('QR-код для Респондентов')
        await msg.answer_photo(photo=img, caption=data)

@router.message(Reg.name)
async def start_reg_1(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_reg = data['group']
    if user_reg == 'resp' or user_reg == 'analitic':
        await state.set_state(Reg.num)
        await state.update_data(name=msg.text)
        key = [['Правильно', 'Изменить']]
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
    if msg.text == 'Правильно':
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
    await msg.answer('Благодарим за регистрацию', reply_markup=key_no())
    set_reg(data['id'], data['group'])
    set_user(data)
    await state.clear()
    if get_reg(msg.from_user.id) == 'resp':
        key = [
            {
                'Задать вопрос': 'question_text',
            },
            {
                'Отмена': 'cancle'
            }
        ]
        msg_text = f'{html.bold("Дорогой гость!")}'
        msg_text += ' Если у Вас возникнет вопрос, '
        msg_text += f'{html.bold("пишите его прямо сюда")}'
        msg_text += ' и мы как-можно быстрее найдем на него ответ'
        await msg.answer(msg_text, reply_markup=await key_I(key))

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
    msg_tsxt += f'Сообщение отправил Организатор {data["names"]}:'
    msg_tsxt += f'{html.blockquote(msg.text)}'
    if data.get('link', False):
        msg_tsxt += f'{hide_link(data["link"])}'
    await msg.answer(msg_tsxt, reply_markup=await key_I(key))

@router.message(StartSend.link)
async def start_send_5(msg: Message, state: FSMContext):
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
    msg_text += f'Сообщение отправил Организатор {data["names"]}:'
    msg_text += f'{html.blockquote(data["text"])}'
    if data.get('link', False):
        msg_text += f'{hide_link(data["link"])}'
    await msg.answer(msg_text, reply_markup=await key_I(key))

@router.message(Questions.text)
async def start_send_7(msg: Message, state: FSMContext):
    await state.update_data(text = msg.text)
    data = await state.get_data()
    await state.clear()
    if set_questions(data):
        list_temp = get_list_id('analitic')
        names = get_user(msg.from_user.id)[0]
        for i in list_temp:
            i = int(i)
            key = [
                {
                    'Ответить на вопрос в боте': 'msg_answer'
                }, 
                {
                    'Я ответил на этот вопрос устно': 'msg_exit'
                }
            ]
            msg_text = f'{html.bold(names)} интересуется:\n\n'
            msg_text += f'{html.blockquote(msg.text)}'
            msg_text += f'В очереди: {len(get_questions())} шт'
            await bot.send_message(chat_id=i, text=msg_text, 
                                   reply_markup=await key_I(key))
        await msg.answer('Ваш вопрос направлен Организаторам')
    else:
        await msg.answer('Ваш вопрос был потерян!\n'+
                         'Обратитесь пожалуйста к администратору!')

@router.message(Answer.text)
async def start_send_7(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    temp_dict = {
        'names_in': '',
        'names_answer': get_user(msg.from_user.id)[0],
        'msg_temp': data['msg_text'],
        'text': data['text'],
        'text_answer': msg.text
    }
    save_ansver(temp_dict)
    await msg.answer('Ваш ответ сохранён для дальнейшего анализа Организаторами')

@router.message(StartSurvey.text)
async def start_send_1(msg: Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(msg.chat.id, data['msg_temp'])
    await bot.delete_message(msg.chat.id, data['msg_temp']+1)
    await state.update_data(text = msg.text)
    key = [
            {
                'Отправить': 'msg_survey'
            }, 
            {
                'Изменить текст': 'text_survey'
            },
            {
                'Отмена': 'cancle'
            }
        ]
    msg_tsxt = html.bold('Проверьте Ваш опрос перед отправкой:\n\n')
    msg_tsxt += f'Опрос отправил Организатор {data["names"]}:'
    msg_tsxt += f'{html.blockquote(msg.text)}'
    await msg.answer(msg_tsxt, reply_markup=await key_I(key))

@router.callback_query(F.data == 'question_list')
async def start_question_list(call: CallbackQuery, state: FSMContext):
    await call.answer()
    temp_questions = get_questions()
    await call.message.delete()
    await call.message.answer(f'Имеются вопросы в кол-ве {len(temp_questions)} шт.\n'+
                              'Функция ещё будет дописываться')

@router.callback_query(F.data == 'send')
async def start_send_0(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.text)    
    await state.update_data(names = get_user(call.from_user.id)[0])
    await state.update_data(msg_temp = call.message.message_id)
    await call.message.edit_text('Введите текст сообшения')

@router.callback_query(F.data == 'msg_send')
async def start_send_2(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    data = await state.get_data()
    list_resp = get_list_id()
    msg_text = f'Сообщение отправил Организатор {data["names"]}:'
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
    await call.message.answer('Произведена рассылка сообщения гостям')
    await state.clear()

@router.callback_query(F.data == 'msg_survey')
async def start_send_2(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    data = await state.get_data()
    list_resp = get_list_id()
    msg_text = f'Опрос отправил Организатор {data["names"]}:'
    msg_text += f'{html.blockquote(data["text"])}'
    key = [
            {
                'У меня есть ответ': 'survey_text'
            }
        ]
    for i in list_resp:
        i = int(i)
        await bot.send_message(chat_id=i, text=msg_text, reply_markup= await key_I(key))
    await call.message.answer('Произведена рассылка опроса гостям')
    await state.clear()

@router.callback_query(F.data == 'text_edit')
async def start_send_3(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.text)
    await state.update_data(msg_temp = call.message.message_id)
    data = await state.get_data()
    await call.message.edit_text('Текст Вашего сообщения:\n'
                                 f'{data["text"]}\n\n'
                                 +'Введите текст сообшения')

@router.callback_query(F.data == 'text_survey')
async def start_send_3(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSurvey.text)
    await state.update_data(msg_temp = call.message.message_id)
    data = await state.get_data()
    await call.message.edit_text('Текст Вашего опроса:\n'
                                 f'{data["text"]}\n\n'
                                 +'Введите текст опроса')

@router.callback_query(F.data == 'link')
async def start_send_4(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSend.link)
    await state.update_data(msg_temp = call.message.message_id)
    data = await state.get_data()
    await call.message.edit_text('Текст Вашего сообщения:\n'
                                 f'{data["text"]}\n\n'
                                 +'Введите ссылку для добавления в сообшение')

@router.callback_query(F.data == 'survey_text')
async def start_sen_6(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Answer.text)
    await state.update_data(id = call.from_user.id)
    print(call.message.text)
    temp_text, text = call.message.text.split(':')
    await state.update_data(msg_text = temp_text)
    await state.update_data(text = text)
    await call.message.answer('Опишите свой вариант ответа')

@router.callback_query(F.data == 'question_text')
async def start_sen_6(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Questions.text)
    await state.update_data(id = call.from_user.id)
    await state.update_data(msg_text = call.message.text)
    await call.message.answer('Опишите свой вопрос и Организаторы Вам ответят, как можно скорее')

@router.callback_query(F.data == 'survey')
async def start_survey(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(StartSurvey.text)  
    await state.update_data(names = get_user(call.from_user.id)[0])
    await state.update_data(msg_temp = call.message.message_id)
    await call.message.edit_text('Введите текст вопроса')

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
    await msg.answer('Вы правда хотите удалить свои данные из конференции? Вам придётся заново регистрироваться, если у Вас появятся вопросы!', 
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
    msg_text = 'Бот МОДЕРАТОР предназначен для оперативного сбора данных от гостей.\n\n'
    msg_text += 'Для выхода из конференции нажмите /stop'
    await msg.answer(msg_text)

@router.message(AnswerSend.text_answer)
async def message_handler_1(msg: Message, state: FSMContext):
    await state.update_data(text_answer = msg.text)
    data = await state.get_data()
    del_answer(data['text'])
    save_ansver(data)
    await state.clear()
    list_temp = get_list_id('analitic')
    msg_text = 'Вам поступил ответ от '
    msg_text += f'{html.bold(data["names_answer"])} на Ваш вопрос:\n'
    msg_text += f'{data["text"]}'
    msg_text += f'\nОтвет: \n\n{data["text_answer"]}'
    key = [
            {
                'Уточнить ответ': 'msg_answer_resp'
            }
        ]
    await bot.send_message(chat_id=data['id_in'], text=msg_text, 
                           reply_markup=await key_I(key))
    await msg.delete()
    await bot.delete_message(msg.chat.id, msg.message_id-1)
    for i in list_temp:
        i = int(i)
        msg_text = f'Вопрос:\n{data["text"]}\nзакрыт: '
        msg_text += f'{html.bold(data["names_answer"])}'
        msg_text += f'\nВ очереди: {len(get_questions())} шт'
        await bot.send_message(chat_id=i, text=msg_text)

@router.callback_query(F.data == 'msg_answer_resp')
async def msg_answer(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.set_state(Questions.text)
    await state.update_data(id_answer = call.from_user.id)
    await state.update_data(names_answer = get_user(call.from_user.id)[0])
    temp_text = call.message.text.lstrip('Вам поступил ответ от ')
    temp_text = temp_text.split(' на Ваш вопрос:\n')
    temp_text.append('')
    temp_text[1], temp_text[2] = temp_text[1].split('\n\nОтвет: \n')
    await state.update_data(id = call.from_user.id)
    await state.update_data(msg_text = temp_text[2])
    await call.message.answer('Опишите, что Вы хотите уточнить и Организаторы ответят, как можно скорее')

@router.callback_query(F.data == 'msg_answer')
async def msg_answer(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.set_state(AnswerSend.text_answer)
    await state.update_data(id_answer = call.from_user.id)
    await state.update_data(names_answer = get_user(call.from_user.id)[0])
    temp_text = call.message.text.split(' интересуется:\n\n')
    temp_text[1], _ = temp_text[1].split('В очереди:')
    temp_text = get_answer(temp_text[1])
    await state.update_data(id_in = temp_text[0])
    await state.update_data(names_in = get_user(temp_text[0])[0])
    await state.update_data(msg_temp = temp_text[1])
    await state.update_data(text = temp_text[2])
    msg_text = 'Напишите ответ на вопрос:\n\n'
    msg_text += f'{html.blockquote(temp_text[2])}'
    await call.message.answer(msg_text)

@router.callback_query(F.data == 'msg_exit')
async def msg_exit(call: CallbackQuery, state: FSMContext):
    await call.answer()
    temp_text = call.message.text.split('\n\n')
    temp_text = temp_text[1]
    temp_text, _ = temp_text.split('В очереди:')
    del_answer(temp_text)
    #to-do добавить сохранение уточнения вопроса

    data = {
        'names_answer': get_user(call.from_user.id)[0],
        'text': temp_text
    }
    list_temp = get_list_id('analitic')
    for i in list_temp:
        i = int(i)
        msg_text = f'Вопрос:\n{data["text"]}\nзакрыт: '
        msg_text += f'{html.bold(data["names_answer"])}'
        msg_text += f'\nВ очереди: {len(get_questions())} шт'
        await bot.send_message(chat_id=i, text=msg_text)

@router.message(F.text)
async def message_handler(msg: Message, state: FSMContext):
    user_reg = get_reg(msg.from_user.id)
    if user_reg == False: 
        await msg.answer('Пройдите регистрацию!')
        return
    data = {
        'id': msg.from_user.id,
        'msg_text': 'Свободный вопрос',
        'text': msg.text
    }
    if set_questions(data):
        list_temp = get_list_id('analitic')
        names = get_user(msg.from_user.id)[0]
        for i in list_temp:
            i = int(i)
            key = [
                {
                    'Ответить на вопрос в боте': 'msg_answer'
                }, 
                {
                    'Я ответил на этот вопрос устно': 'msg_exit'
                }
            ]
            msg_text = f'{html.bold(names)} интересуется:\n\n'
            msg_text += f'{html.blockquote(msg.text)}\n'
            msg_text += f'В очереди: {len(get_questions())} шт'
            await bot.send_message(chat_id=i, text=msg_text, 
                                   reply_markup=await key_I(key))
        await msg.answer('Ваш вопрос направлен Организаторам')
    else:
        await msg.answer('Ваш вопрос был потерян!\n'+
                         'Обратитесь пожалуйста к администратору!')