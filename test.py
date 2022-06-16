from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram import Bot
import os

OWNER_ID = int(os.getenv('OWNERID'))
GROUP_ID = int(os.getenv('GROUPID'))
bot = Bot(token=os.getenv('TOKEN'))
#Классу фильтра должна быть присвоена переменная key
class AdminFilter(BoundFilter):
    key = 'admin'

    def __init__(self, admin):
        self.chat_admin = admin

    async def check(self, message: types.Message):
        chat = [admin.user.id for admin in await bot.get_chat_administrators(GROUP_ID)]
        print(chat)
        for q in chat:
            if q == OWNER_ID:
                print(OWNER_ID)
                return admin
                
            

    
            
        #message.from_user.id = 'OWNERID'
        
        
