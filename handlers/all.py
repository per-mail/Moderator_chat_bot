#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create_bot import dp, bot, conn, cur
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import json, string

from create_bot import bot, GROUP_ID
    



#заносим пользователей в базу и фильтруем чат
#@dp.message_handler()
async def filter_message(message: types.Message, state: FSMContext):    
# проверяем есть ли пользоваель в чс, если да удаляем сообщение
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', '0')")
    conn.commit()
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()           
               
    a = result[0]   # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы         
    d = a[0]
    if d == 1:
        await message.delete()
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вам запрещено писать в чат!')
# проверяем сообщения на наличие ссылок
    for i in (".рф", ".ru", ".com", '.biz'):
        if i in message.text.lower():
            await message.delete()          
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
            result = cur.fetchall()           
               
            a = result[0]   # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы         
            d = a[0]
            if d == 0:
                cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.from_user.id}")                    
                conn.commit()
                await message.answer(f'{message.from_user.first_name} успешно добавлен в ЧС.')
                await state.finish()
    #накладываем ограничения на пользователя
                await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
                await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы получили бан!')   
            
           #if d == 1:                            
                #await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
                #await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вас удалили из группы за нарушение правил!') 
                #await message.answer(f'{message.from_user.first_name} удалён')

        
# проверяем сообщения на наличие мата          
            
#видео о фильтре мата https://www.youtube.com/watch?v=Lgm7pxlr7F0&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=3            
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
       .intersection(set(json.load(open('spisok.json')))) != set():
       await message.delete()
       cur = conn.cursor()
       cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
       result = cur.fetchall()           
               
       a = result[0]        # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы         
           
       d = a[0]
       if d == 0:
                       cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.from_user.id}")                    
                       conn.commit()
                       await message.answer(f'{message.from_user.first_name} успешно добавлен в ЧС.')
                       await state.finish()
                       #накладываем ограничения на пользователя
                       await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
                       await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы получили бан!')   
            
       #if d == 1:                            
                      #await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
                      #await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вас удалили из группы за нарушение правил!') 
                      #await message.answer(f'{message.from_user.first_name} удалён!')


# Вариант закрытая группа(вход по приглашению) приветствие, удаленние записи, внесение в базу, не впускаем пользователей которые в чёрном списке
#@dp.chat_join_request_handler()
async def link(message: types.Message, state: FSMContext):    
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', '0')")
    conn.commit()

    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()
    a = result[0]   # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы            
    d = a[0] 
    if d == 1:
         await bot.decline_chat_join_request(message.chat.id,message.from_user.id)
         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы в чёрном списке группы за нарушение правил!')
    else:          
         await bot.approve_chat_join_request(message.chat.id,message.from_user.id)         
         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в чат!')

  

    
    

def register_handlers_all(dp : Dispatcher):    
    dp.register_message_handler(filter_message)
    dp.register_chat_join_request_handler(link)
    
    


    
    
