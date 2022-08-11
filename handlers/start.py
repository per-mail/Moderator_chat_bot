#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor, Dispatcher
from create import dp, bot
#from create import dp, bot, conn, cur, GROUP_ID, OWNER_ID, BOT_ID
#from aiogram.dispatcher.filters.state import State, StatesGroup
from adm_filter import AdminFilter
from aiogram.types import Message
#from admins_filter import moderators, ADMINS_LIST


async def vchod(message: types.Message):     
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}. Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
        
    #else:
       #await message.answer(f'{message.from_user.first_name}. У Вас нет прав администратора.')
        


def register_handlers_start(dp : Dispatcher):
    dp.register_message_handler(vchod, admin=True, commands=['start', 'старт'])
    
    

     

