# -*- coding: utf-8 -*-


router = Router()




@router.message(Command("start"))
async def start_handler(msg: Message):
    print(dir(msg))
    print(msg.from_user.id)
    print(msg.content_type)
    print(msg.date)
    print(msg.from_user)
    print(msg.message_id)
    print(msg.text)
    #print(dir(html))
    if len(msg.text.split()) > 1:
        #to-do отработка алгоритма начального входа для участников
        pass
        print(msg.text)
        _, new_user = msg.text.split()
        if new_user == 'analitic':
            await msg.answer('Привет! Я бот. Я знаю, что ты Аналитик, что будем делать?')
        elif new_user == 'resp':
            await msg.answer('Добрый день! Я бот, буду помогать оперативно управлять конференцией')
        elif new_user == 'admin':
            await msg.answer('Вы пытаетесь изменить Администратора, подтвердите свои права доступа')

        else:
            await msg.answer('Вы ошиблись с вводом данных')
        return
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой простой ID: {msg.from_user.id}") # 
    await msg.answer(f"Твой жирный ID: {h(msg.from_user.id)}") # 
    await msg.answer(f"Твой курсив ID: {h(msg.from_user.id, 1)}") # 
    await msg.answer(f"Твой код ID: {h(msg.from_user.id, 2)}") # 
    await msg.answer(f"Твой блок ID: {h(msg.from_user.id, 3)}") # 

