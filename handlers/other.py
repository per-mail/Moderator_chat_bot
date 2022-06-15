#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create import dp, bot, conn, cur, GROUP_ID, OWNER_ID, BOT_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import json, string
from filter_chat import IsAdminFilter
from aiogram.types.chat_permissions import ChatPermissions
from admins_filter import moderators, ADMINS_LIST

# Окрытая группа приветствие, удаленние записи, внесение в базу, удаление пользователей которые в чёрном списке
#@dp.message_handler(content_types=["new_chat_members"])
async def on_user(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE (user_id="{message.from_user.id}")')
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', 'False', 'False')")
    conn.commit()
    await message.delete()
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.from_user.id}")
    result = cur.fetchall()           
               
    a = result[0] # здесь мы избавляемся от запятой         
    d = a[0] 
    if d == 'True':
         #await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.from_user.id)
         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Вы в чёрном списке группы за нарушение правил!')
    else:
         await message.answer(f'{message.from_user.first_name}!\nДобро пожаловать в чат !')


#  удаленние записи об уходе пользователя из группы, прощальное письмо
#@dp.message_handler(content_types=["left_chat_member"])
async def out(message: types.Message):     
    await message.delete()
# проверяем есть ли пользователь в списке админов    
# получаем список админов 2 способ, мой с функцией
    moderators()
    if message.from_user.id not in ADMINS_LIST:  # проверяем что это пользователь сам удаляется из чата     
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} жаль, что Вы покинули чат. Возвращайтесь обратно!.') 
                      

    
              
                      
#  удаление из группы
#@dp.message_handler(is_admin=True, commands=["weg", "вег"], commands_prefix="!/")
async def weg(message: types.Message, state: FSMContext):
    if not message.reply_to_message:        
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} выберите кого нужно удалить?')
        await message.delete()        
        return
    await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)
    await message.delete()
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} не найден в базе данных.')        
        await state.finish()  
    else:              
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} удалён!')
        await bot.send_message(message.reply_to_message.from_user.id, f'{message.reply_to_message.from_user.first_name}. Вас удалили из группы за нарушение правил!')
        a = result[0]  # здесь мы избавляемся от запятой        
        d = a[0]
        if d == 'False':
                cur.execute(f"UPDATE users SET block = 'True' WHERE user_id = {message.reply_to_message.from_user.id}")                    
                conn.commit()                       
                await state.finish()
        else:
                await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} уже получал предупреждение.')



#  удаление из группы баном
#@dp.message_handler(is_admin=True, commands=["wegban"], commands_prefix="!/")
async def wegban(message: types.Message):
    if not message.reply_to_message:        
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} выберите кого нужно удалить?')
        await message.delete()
        return
    else:    
         await message.delete()
         await bot.ban_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)
         await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} удалён!')
         await bot.send_message(message.reply_to_message.from_user.id, f'{message.reply_to_message.from_user.first_name}. Вас удалили из группы за нарушение правил!')
                 

# убираем бан в Телеграм
#@dp.message_handler(is_admin=True, commands=["unban"], commands_prefix="!/")
async def unban(message: types.Message):
    if not message.reply_to_message:        
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} выберите кого нужно удалить?')
# 2 вариант удаления строки
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    else:
# 2 вариант удаления строки        
        await message.bot.delete_message(GROUP_ID, message.message_id)
        await bot.unban_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} разбанен')
        await bot.send_message(message.reply_to_message.from_user.id, f'{message.reply_to_message.from_user.first_name}. Вам сняли бан!')
        

# заносим пользователя в чёрный список в чате
#@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message, state: FSMContext):
    if not message.reply_to_message:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} выберите кого нужно забанить?')
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    await message.delete()
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} не найден в базе данных.')
        await state.finish() 
    else:
        a = result[0] # здесь мы избавляемся от запятой                          
        d = a[0]
        if d == 'False':
            cur.execute(f"UPDATE users SET block = 'True' WHERE user_id = {message.reply_to_message.from_user.id}")
            conn.commit()
            await bot.send_message(message.reply_to_message.from_user.id, f'{message.reply_to_message.from_user.first_name}. Администратор добавил Вас в чёрный список!')
            await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} забанен.')
            await state.finish()         
        else:
            await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} уже получил бан')
            await state.finish()


                

# убираем пользователя из чёрного списка в чате
#@dp.message_handler(is_admin=True, commands=["free"], commands_prefix="!/")
async def free(message: types.Message, state: FSMContext):
    if not message.reply_to_message:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Выберите кого нужно разбанить?')
        await message.delete()
        return
    await message.bot.delete_message(GROUP_ID, message.message_id)
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} не найден в базе данных.')
        await state.finish() 
    else:
        a = result[0]      # здесь мы избавляемся от запятой                            
        d = a[0]
        if d == 'True':
            cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.reply_to_message.from_user.id}")
            conn.commit()
            await bot.send_message(message.reply_to_message.from_user.id, f'{message.reply_to_message.from_user.first_name}. Администратор убрал Вас из чёрного списка!')
            await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} разбанен.')
            await state.finish()         
        else:
            await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} не получал бан')
            await state.finish()


#  удаление из базы данных
#@dp.message_handler(is_admin=True, commands=["bd"], commands_prefix="!/")
async def baza(message: types.Message, state: FSMContext):
    if not message.reply_to_message:        
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Выберите кого нужно удалить из базы?')
        await message.bot.delete_message(GROUP_ID, message.message_id)
        return
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
    result = cur.fetchall()
    conn.commit()
    if len(result) == 0:
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} не найден в базе данных.')
        await message.delete()    
        await state.finish()  
    else:
        await message.delete()
        cur.execute(f"DELETE FROM users WHERE user_id = {message.reply_to_message.from_user.id}")
        conn.commit()
        await bot.send_message(message.from_user.id, f'{message.reply_to_message.from_user.first_name} удалён из базы!')
        await state.finish() 

# ограничиваем пользователя пользователя метод для супергрупп
#@dp.message_handler(is_admin=True, commands=["res"], commands_prefix="!/")
async def cmd_res(message: types.Message):
    await bot.restrict_chat_member(GROUP_ID, message.reply_to_message.from_user.id)
    await message.delete()

# ограничиваем пользователя пользователя метод для супергрупп
#@dp.message_handler(is_admin=True, commands=["unres"], commands_prefix="!/")
async def cmd_unres(message: types.Message):
    await bot.restrict_chat_member(GROUP_ID, message.reply_to_message.from_user.id,ChatPermissions(can_send_messages=True, can_send_media_messages=True,can_send_other_messages=True, can_add_web_page_previews=True)) 
    await message.delete()   
   
#  повышаем или понижаем пользователя метод для супергрупп
#@dp.message_handler(is_admin=True, commands=["prom"], commands_prefix="!/")
async def cmd_prom(message: types.Message):
    await bot.promote_chat_member(message.from_user.id, message.reply_to_message.from_user.id)
    await message.delete()          


#  получаем user.id пользователя
#@dp.message_handler(is_admin=True, commands=["id"], commands_prefix="!/")
async def cmd_id(message: types.Message):
    await bot.send_message(message.from_user.id, message.reply_to_message.from_user.id)
    await message.delete()

#  получаем user.name пользователя
#@dp.message_handler(is_admin=True, commands=["un"], commands_prefix="!/")
async def cmd_username(message: types.Message):
    await bot.send_message(message.from_user.id, message.reply_to_message.from_user.username)
    await message.delete()

#  получаем first_name пользователя
#@dp.message_handler(is_admin=True, commands=["fn"], commands_prefix="!/")
async def cmd_first_name(message: types.Message):
    await bot.send_message(message.from_user.id, message.reply_to_message.from_user.first_name)
    await message.delete()
    




def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(on_user, content_types=["new_chat_members"])    
    dp.register_message_handler(out, content_types=["left_chat_member"])
    dp.register_message_handler(weg, chat_admin=True, commands=["weg", "вег"], commands_prefix="!/")
    dp.register_message_handler(wegban, chat_admin=True, commands=["wegban"], commands_prefix="!/")
    dp.register_message_handler(unban, chat_admin=True, commands=["unban"], commands_prefix="!/")
    dp.register_message_handler(ban, chat_admin=True, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(free, chat_admin=True, commands=["free"], commands_prefix="!/")
    dp.register_message_handler(cmd_id, chat_admin=True, commands=["id"], commands_prefix="!/")
    dp.register_message_handler(cmd_username, chat_admin=True, commands=["un"], commands_prefix="!/")    
    dp.register_message_handler(baza, chat_admin=True, commands=["bd"], commands_prefix="!/")
    dp.register_message_handler(cmd_first_name, chat_admin=True, commands=["fn"], commands_prefix="!/")
    dp.register_message_handler(cmd_prom, chat_admin=True, commands=["prom"], commands_prefix="!/")
    dp.register_message_handler(cmd_res, chat_admin=True, commands=["res"], commands_prefix="!/")
    dp.register_message_handler(cmd_unres, chat_admin=True, commands=["unres"], commands_prefix="!/")
    
    
    





                      
                     
                      

    
    
