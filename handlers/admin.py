#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher

from create import dp, bot, conn, cur, GROUP_ID, OWNER_ID, BOT_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from adm_filter import AdminFilter

from aiogram.types.chat_permissions import ChatPermissions
from admins_filter import moderators, ADMINS_LIST

#Перед тем как создать какое-либо состояние, нам нужно создать класс, где мы поочередно опишем все states
#чтобы потом без проблем переключаться между ними
class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()
    admin_in = State()
    admin_out = State()


#@dp.message_handler(state='*', text='Назад')
async def back(message: Message):

    #if message.from_user.id in ADMINS_LIST:  
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer('Основное меню', reply_markup=keyboard)
    #else:
        #await message.answer(f'{message.from_user.first_name}. Вам не доступна эта функция')



#@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):    
                
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))        
        await message.answer(f'{message.from_user.first_name} напиши текст рассылки или нажми кнопку назад', reply_markup=keyboard)
        await dialog.spam.set()#перключаем состояния
            
        
        
#Здесь и далее берём user_id из message.text из текста сообщения или из текста который приходит из базы.      

# этот блок нужен, чтобы приостановить исполнение кода и ввести текст рассылки
#@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: #FSMContext): state: FSMContext для того, чтобы мы могли записывать данные пользователя в память
    if  message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer(f'{message.from_user.first_name}. Рассылка прервана', reply_markup=keyboard)
#всё завершаем методом finish()
        await state.finish()
    else:
        cur = conn.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE admin = 'False'")
        #cur.execute(f'SELECT user_id FROM users')
        spam_base = cur.fetchall()
        print(spam_base)
        for q in range(len(spam_base)):
           print(spam_base[q][0])
        for q in range(len(spam_base)):
            await bot.send_message(spam_base[q][0], message.text)          
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer(f'{message.from_user.first_name}. Рассылка завершена', reply_markup=keyboard)
        await state.finish()
        
#@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            f'{message.from_user.first_name}. Введите id пользователя, которого нужно заблокировать или нажми кнопку назад',
            reply_markup=keyboard)
#подключаемся к базе
        await dialog.blacklist.set()
        


#@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
      if message.text.isdigit() and message.text != 'Назад': # проверяем что все символы цифры  и что сообщение не равно Назад
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}') #берём user_id из message.text и ищём есть ли он в базе
            result = cur.fetchall()
            
#Метод connect.commit() фиксирует текущую транзакцию. Если не вызывать этот метод, то все, что сделано после последнего вызова connect.commit(), не будет видно из других соединений с базой данных.
#Если встретили ситуацию при которой не видны данные, которые были переданы в базу данных, то необходимо убедится, что метод connect.commit был вызван.

            #conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой
                d = a[0]                
                if d == 'False':
                    cur.execute(f"UPDATE users SET block = 'True' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'Пользователь успешно добавлен в ЧС.', reply_markup=keyboard)
                    await state.finish()
                    #вводим ограничения на пользователя
                    await bot.restrict_chat_member(GROUP_ID, message.text)#берём user_id из message.text
                    await bot.send_message(message.text, 'Администратор добавил Вас в чёрный список!')                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Данный пользователь уже получил бан', reply_markup=keyboard)
                    #вводим ограничения на пользователя
                    await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.text) #берём user_id из message.text
                    await bot.send_message(message.text, 'Вы получили ограничения')
                    await state.finish()
                    

      else:
            await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
            await message.answer(f'{message.from_user.first_name}. Операция прервана', reply_markup=keyboard)
#
            await state.finish()
             

        

#@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):  
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                f'{message.from_user.first_name}. Введите id пользователя, которого нужно разблокировать или нажми кнопку назад',
                reply_markup=keyboard)
            await dialog.whitelist.set()



#@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
      if message.text.isdigit() and message.text != 'Назад': # проверяем что все символы цифры  и что сообщение не равно Назад
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}')
            result = cur.fetchall()
            #conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой  
                d = a[0]
                if d == 'True':
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET block = 'False' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в списка админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Пользователь успешно разбанен.', reply_markup=keyboard)
                    await state.finish()
                    #берём user_id из message.text
                    await bot.restrict_chat_member(GROUP_ID, message.text,ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True))
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'{message.from_user.first_name}. не получал бан.', reply_markup=keyboard)
                    await state.finish()
                  
      else:

            await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
            await message.answer(f'{message.from_user.first_name}. Операция прервана', reply_markup=keyboard)
#
            await state.finish()


async def admin_in(message: types.Message, state: FSMContext):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            f'{message.from_user.first_name}. Введите id пользователя, которого нужно добавить в список или нажми кнопку назад', reply_markup=keyboard)
            
#подключаемся к базе
        await dialog.admin_in.set()

   
#@dp.message_handler(state=dialog.blacklist)
async def adminin(message: types.Message, state: FSMContext):     
      if message.text.isdigit() and message.text != 'Назад': # проверяем что все символы цифры и что сообщение не равно Назад
            cur = conn.cursor()
            cur.execute(f'SELECT admin FROM users WHERE user_id = {message.text}') #берём user_id из message.text и ищём есть ли он в базе
            result = cur.fetchall()
            #conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой
                d = a[0]                
                if d == 'False':
                    cur.execute(f"UPDATE users SET admin = 'True' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'Пользователь успешно добавлен в список админов.', reply_markup=keyboard)
                    ADMINS_LIST.append(message.text)                    
                    await state.finish()
                   
                    await bot.send_message(message.text, 'Администратор добавил Вас в список админов!')                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Данный пользователь уже есть списке админов!', reply_markup=keyboard)
                    await state.finish()
             
      else:
            await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
            await message.answer(f'{message.from_user.first_name}. Операция прервана', reply_markup=keyboard)
#
            await state.finish()

#@dp.message_handler(content_types=['text'], text='Убрать из списка\n админов')
async def admin_out(message: types.Message, state: FSMContext): 
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                f'{message.from_user.first_name}. Введите id пользователя, которого нужно убрать из списка админов или нажми кнопку назад', reply_markup=keyboard)                
            await dialog.admin_out.set()
   

async def adminout(message: types.Message, state: FSMContext):
      if message.text.isdigit() and message.text != 'Назад': # проверяем что все символы цифры  и что сообщение не равно Назад
            cur = conn.cursor()
            cur.execute(f'SELECT admin FROM users WHERE user_id = {message.text}')
            result = cur.fetchall()
            #conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой  
                d = a[0]
                if d == 'True':
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET admin = 'False' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Пользователь успешно удалён из списка админов', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были удалены из списка админов')
                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'{message.from_user.first_name}.нет в списке админов.', reply_markup=keyboard)
                    await state.finish()
               
      else:
          
            await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
            keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
            keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
            await message.answer(f'{message.from_user.first_name}. Операция прервана', reply_markup=keyboard)
#
            await state.finish()


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(spam, admin=True, content_types=['text'], text='Рассылка')
    dp.register_message_handler(start_spam, admin=True, state=dialog.spam)    
    dp.register_message_handler(hanadler, admin=True, content_types=['text'], text='Добавить в ЧС')
    dp.register_message_handler(proce, admin=True, state=dialog.blacklist)
    dp.register_message_handler(hfandler, admin=True, content_types=['text'], text='Убрать из ЧС')
    dp.register_message_handler(proc, admin=True, state=dialog.whitelist)    
    dp.register_message_handler(admin_in, admin=True, content_types=['text'], text='Добавить в список админов')
    dp.register_message_handler(adminin, admin=True, state=dialog.admin_in)
    dp.register_message_handler(admin_out, admin=True, content_types=['text'], text='Убрать из списка админов')
    dp.register_message_handler(adminout, admin=True, state=dialog.admin_out)
    dp.register_message_handler(back, admin=True, content_types=['text'], text='Назад')
    
