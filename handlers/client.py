#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor, Dispatcher
from create_bot import dp, bot, conn, cur, BOT_ID, OWNER_ID, GROUP_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from filters import IsAdminFilter
from test import moderators

async def vchod(message: types.Message):

    
# проверяем на право доступа
# получаем список админов 1 способ
    #ADMINS_LIST = [admin.user.id for admin in await bot.get_chat_administrators(GROUP_ID)]    
# получаем список админов 2 способ, мой
    #cur = conn.cursor()
    #cur.execute(f"SELECT user_id FROM users WHERE admin = 'True'")
    #result = cur.fetchall()# получаем id пользователей с правом доступа из базы    
    #conn.commit()
    # создаём ADMINS_LIST и вносим сразу OWNER_ID и BOT_ID в список админов
    #ADMINS_LIST = [OWNER_ID, BOT_ID]    
    #for q in result:
       #w = q[0] # здесь мы избавляемся от запятой        
       #ADMINS_LIST.append(w)
    
    moderators()
    #ADMINS_LIST = moderators.ADMINS_LIST
    if message.from_user.id == OWNER_ID:           
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
        
    else:
        await message.answer(f'{message.from_user.first_name}. У Вас нет прав администратора.')
        
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
    rez = cur.fetchone()
    if rez is None:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', 'False', 'False')")
    conn.commit()             
        

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(vchod, commands=['start', 'старт'])
    
    

     

