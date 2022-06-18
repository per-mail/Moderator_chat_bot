from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from create import conn, cur, OWNER_ID, BOT_ID, GROUP_ID

# обьявляем переменную
# здесь переменной админ можно присвоить любое значение, 'admin' необязательно

admin = 'admin'

# создаём список по умолчанию с владельцем и ботом 
DEFAULT_LIST = [BOT_ID] 
# создаём список админов
ADMINS_LIST = [] 
#Классу фильтра должна быть присвоена переменная key
class AdminFilter(BoundFilter):
    key = 'admin'
#https://overcoder.net/q/3496/python-init-%D0%B8-self-%D1%87%D1%82%D0%BE-%D0%BE%D0%BD%D0%B8-%D0%B4%D0%B5%D0%BB%D0%B0%D1%8E%D1%82
#переменная self представляет экземпляр объекта BoundFilter в  Python в отличии от большинства других языков прогаммирования этот парамнтр передаётся явно
#Установка этих переменной как self.admin устанавливает её как член объекта BoundFilter, и они доступны во время жизни объекта.
#__init_ - это подобие конструктора в других языках, это специальный метод, вызываемый автоматически, когда создается объект класса AdminFilter
    def __init__(self, admin):
        self.admin_test = admin
# получаем список админов из Телеграмм  
    #async def check(self, message: types.Message):
      
        #ch = [admin.user.id for admin in await bot.get_chat_administrators(GROUP_ID)]        for q in ch:
        #if q == message.from_user.id:
            #return admin
        
                           

# получаем список админов из базы    
    async def check(self, message: types.Message):
# удаляем старый список админов
       ADMINS_LIST.clear()
# создаём ADMINS_LIST и добавляем в список по умолчанию владельца и бота  
       ADMINS_LIST.extend(DEFAULT_LIST)
       cur = conn.cursor()
       cur.execute(f"SELECT user_id FROM users WHERE admin = 'True'")
       result = cur.fetchall()# получаем id пользователей с правом доступа из базы    
       conn.commit()    
    # В ADMINS_LIST  вносим админов из базы       
       for q in result:
          w = q[0] # здесь мы избавляемся от запятой        
          ADMINS_LIST.append(w)
          for q in ADMINS_LIST:
             if q == message.from_user.id:
                return admin

    
      
        
        
