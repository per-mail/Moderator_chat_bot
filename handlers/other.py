#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create_bot import dp, bot, conn, cur
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import json, string
from filters import IsAdminFilter
from create_bot import bot, GROUP_ID



# приветствие, удаленние записи, внесение в базу, удаление пользователей которые в чёрном списке
#@dp.message_handler(content_types=["new_chat_members"])
async def on_user(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
    conn.commit()
    await message.delete()
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()           
               
    a = result[0]   # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы            
    d = a[0] 
    if d == 1:
         await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
         await bot.send_message(message.from_user.id, 'Вы в чёрном списке группы за нарушение правил!')
    else:
         await message.answer('Добро пожаловать в чат\nПредставьтесь пожалуйста!') 
                      


#  удаление
#@dp.message_handler(is_admin=True, commands=["weg"], commands_prefix="!/")
async def weg(message: types.Message, state: FSMContext):
    if not message.reply_to_message:        
        await bot.send_message(message.from_user.id, "удалить?")
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, 'Такой пользователь не найден в базе данных.')
        await message.bot.delete_message(GROUP_ID, message.message_id)
        await state.finish()  
    else:
        await message.bot.delete_message(GROUP_ID, message.message_id)
        await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)
        await message.reply_to_message.reply("Полльзователь удалён")
        await bot.send_message(message.reply_to_message.from_user.id, 'Вас удалили из группы за нарушение правил!')
        a = result[0]  # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы         
        d = a[0]
        if d == 0:
                cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.reply_to_message.from_user.id}")                    
                conn.commit()                       
                await state.finish()
        else:
                await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.id} уже получал предупреждение.')
            
                  
    

# заносим пользователя в чёрный список в чате
#@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message, state: FSMContext):
    if not message.reply_to_message:
        await bot.send_message(message.from_user.id, "Кого нужно забанить?")
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    await message.bot.delete_message(GROUP_ID, message.message_id)
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, 'Такой пользователь не найден в базе данных.')
        await state.finish() 
    else:
        a = result[0]      # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы                          
        d = a[0]
        if d == 0:
            cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.reply_to_message.from_user.id}")
            conn.commit()
            await bot.send_message(message.reply_to_message.from_user.id, 'Администратор добавил Вас в чёрный список!')
            await bot.send_message(message.from_user.id, 'Пользователь забанен.')
            await state.finish()         
        else:
            await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.username} уже получил бан')
            await state.finish()
            
                

# убираем пользователя из чёрного списка в чате
#@dp.message_handler(is_admin=True, commands=["free"], commands_prefix="!/")
async def free(message: types.Message, state: FSMContext):
    if not message.reply_to_message:
        await bot.send_message(message.from_user.id, "Кого нужно разбанить?")
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    await message.bot.delete_message(GROUP_ID, message.message_id)
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, 'Такой пользователь не найден в базе данных.')
        await state.finish() 
    else:
        a = result[0]      # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы                          
        d = a[0]
        if d == 1:
            cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.reply_to_message.from_user.id}")
            conn.commit()
            await bot.send_message(message.reply_to_message.from_user.id, 'Администратор убрал Вас из чёрного списка!')
            await bot.send_message(message.from_user.id, 'Пользователь разбанен.')
            await state.finish()         
        else:
            await bot.send_message(message.from_user.id, 'Данный пользователь не получал бан.')
            await state.finish()


#  получаем user.id пользователя
#@dp.message_handler(is_admin=True, commands=["id"], commands_prefix="!/")
async def cmd_id(message: types.Message):
    await bot.send_message(message.from_user.id, message.reply_to_message.from_user.id)
    await message.bot.delete_message(GROUP_ID, message.message_id)

#  получаем user.name пользователя
#@dp.message_handler(is_admin=True, commands=["un"], commands_prefix="!/")
async def cmd_username(message: types.Message):
    await bot.send_message(message.from_user.id, message.reply_to_message.from_user.username)
    await message.bot.delete_message(GROUP_ID, message.message_id)
    




def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(on_user, content_types=["new_chat_members"])
    dp.register_message_handler(weg, is_admin=True, commands=["weg"], commands_prefix="!/")
    dp.register_message_handler(ban, is_admin=True, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(free, is_admin=True, commands=["free"], commands_prefix="!/")
    dp.register_message_handler(cmd_id, is_admin=True, commands=["id"], commands_prefix="!/")
    dp.register_message_handler(cmd_username, is_admin=True, commands=["un"], commands_prefix="!/")
    





                      
                     
                      

    
    
