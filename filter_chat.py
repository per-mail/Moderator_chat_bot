from aiogram import types
from aiogram.dispatcher.filters import BoundFilter



#Классу фильтра должна быть присвоена переменная key
class IsAdminFilter(BoundFilter):
    key = 'chat_admin'

    def __init__(self, chat_admin):
        self.chat_admin = chat_admin


    async def check(self, message: types.Message):        
        chat = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return chat.is_chat_admin()
