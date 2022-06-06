#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor, Dispatcher
from create_bot import dp, bot, conn, cur, ADMIN
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message



async def privet(message: types.Message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == ADMIN:        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
        
    else:
        await message.answer(f'{message.from_user.first_name}. У Вас нет прав администратора.')
        if result is None:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM users WHERE (user_id='{message.from_user.id}')")
            rez = cur.fetchone()
            if rez is None:
                cur.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', '0')")
            conn.commit()
            
        

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(privet, commands=['start'])
    

     

