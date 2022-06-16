#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor, Dispatcher
from create import dp, bot, conn, cur, BOT_ID, OWNER_ID, GROUP_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from test import AdminFilter

#from admins_filter import moderators, ADMINS_LIST


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
# получаем список админов 2 способ, мой с функцией
    #moderators() 
    #if message.from_user.id in ADMINS_LIST:           
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
        
    #else:
       # await message.answer(f'{message.from_user.first_name}. У Вас нет прав администратора.')
        


def register_handlers_start(dp : Dispatcher):
    dp.register_message_handler(vchod, admin=True, commands=['start', 'старт'])
    
    

     

