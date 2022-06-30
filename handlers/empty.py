#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create import dp, bot, conn, cur, GROUP_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import json, string
from Talk import speak

    

#заносим пользователей в базу и фильтруем чат
#@dp.message_handler()
async def filter_message(message: types.Message, state: FSMContext):    
# проверяем есть ли пользоваель в чс, если да удаляем сообщение
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', 'False', 'False')")
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()           
               
    a = result[0]   # здесь мы извлекаем избавляемся от запятой         
    d = a[0]
    if d == 'True':
        await message.delete()
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вам запрещено писать в чат!')
        
# проверяем сообщения на наличие ссылок и ругательств
    for i in (".рф", ".ru", ".com", '.biz'):
        if i in message.text.lower() or {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('spisok.json')))) != set():                      
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
            result = cur.fetchall()    
            a = result[0]   # здесь мы извлекаем избавляемся от запятой        
            d = a[0]
            if d == 'False':
                await message.delete()
                cur.execute(f"UPDATE users SET block = 'True' WHERE user_id = {message.from_user.id}")                    
                await message.answer(f'{message.from_user.first_name} успешно добавлен в ЧС.')
                await state.finish()  
                await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы получили предупреждение')   
            
            else:
                await message.delete()
                #накладываем ограничения на пользователя
                await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
                await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы получили ограничения за нарушение правил!') 
 
# общение с ботом мпортируем функцию speak и передаём в неё message.text из чата
        else:
             reply = speak(message.text)
             await message.reply(speak(message.text))
             await bot.send_message(GROUP_ID, reply)
             
            
# Вариант закрытая группа(вход по приглашению) приветствие, удаленние записи, внесение в базу, не впускаем пользователей которые в чёрном списке
#@dp.chat_join_request_handler()
async def link(message: types.Message, state: FSMContext):    
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', 'False', 'False')")
    

    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()
    a = result[0]   # здесь мы избавляемся от запятой            
    d = a[0] 
    if d == 'True':
         await bot.decline_chat_join_request(message.chat.id,message.from_user.id)
         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы в чёрном списке группы за нарушение правил!')
    else:          
         await bot.approve_chat_join_request(message.chat.id,message.from_user.id)         
         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в чат!')

  

    
    

def register_handlers_empty(dp : Dispatcher):    
    dp.register_message_handler(filter_message)
    dp.register_chat_join_request_handler(link)
    
    


    
    
