#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create_bot import dp, bot, conn, cur
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from create_bot import bot, ADMIN, GROUP_ID



class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()



#@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
    if message.from_user.id == ADMIN:        
        await dialog.spam.set()
        await message.answer(f'{message.from_user.first_name} напиши текст рассылки')
    else:
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата')
       
#Здесь и далее берём user_id из message.text из текста сообщения или из текста который приходит из базы.      

#@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Главное меню', reply_markup=keyboard)
        await state.finish()
    else:
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM users')
        spam_base = cur.fetchall()
        print(spam_base)
        for q in range(len(spam_base)):
            print(spam_base[q][0])
        for q in range(len(spam_base)):
            await bot.send_message(spam_base[q][0], message.text)
        await message.answer(f'{message.from_user.first_name}. Рассылка завершена')
        await state.finish()


#@dp.message_handler(state='*', text='Назад')
async def back(message: Message):
    if message.from_user.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Главное меню', reply_markup=keyboard)
    else:
        await message.answer(f'{message.from_user.first_name}. Вам не доступна эта функция')


#@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            f'{message.from_user.first_name}. Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже',
            reply_markup=keyboard)
#подключаемся к базе
        await dialog.blacklist.set()
        


#@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        await message.answer('Отмена!', reply_markup=keyboard)
        await state.finish()
    else:        
        if message.text.isdigit():# проверяем что все символы цифры
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}') #берём user_id из message.text и ищём есть ли он в базе
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы    
                d = a[0]                
                if d == 0:
                    cur.execute(f'UPDATE users SET block = 1 WHERE user_id = {message.text}')
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer(f'{message.from_user.first_name} успешно добавлен в ЧС.', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Администратор добавил Вас в чёрный список!')                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Данный пользователь уже получил бан', reply_markup=keyboard)
                    #вводим ограничения на пользователя
                    await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.text)#берём user_id из message.text
                    await bot.send_message(message.text, 'Вы получили ограничения')
                    await state.finish()
        else:
            await message.answer(f'{message.from_user.first_name}. Ты вводишь буквы...\n\nВведи ID')


#@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                f'{message.from_user.first_name}. Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже',
                reply_markup=keyboard)
            await dialog.whitelist.set()


#@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
    if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}')
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы извлекаем 1 или 0 из 1, или 0, которая приходит из базы    
                d = a[0]
                if d == 1:
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer('Пользователь успешно разбанен.', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    await message.answer(f'{message.from_user.first_name}. не получал бан.', reply_markup=keyboard)
                    await state.finish()
    else:
          await message.answer(f'{message.from_user.first_name}. Ты вводишь буквы...\n\nВведи ID')
          

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(spam, content_types=['text'], text='Рассылка')
    dp.register_message_handler(start_spam, state=dialog.spam)
    dp.register_message_handler(back, state='*', text='Назад')
    dp.register_message_handler(hanadler, content_types=['text'], text='Добавить в ЧС')
    dp.register_message_handler(proce, state=dialog.blacklist)
    dp.register_message_handler(hfandler, content_types=['text'], text='Убрать из ЧС')
    dp.register_message_handler(proc, state=dialog.whitelist)
    
    
