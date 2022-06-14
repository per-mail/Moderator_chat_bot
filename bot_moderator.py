import logging
from aiogram.utils import executor

from create_bot import dp



from aiogram import types, executor,  Dispatcher
from create_bot import dp, bot, conn, cur
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from create_bot import bot, GROUP_ID, OWNER_ID, BOT_ID
# log
logging.basicConfig(level=logging.INFO)

# функция оповещение о старте
async def on_startup(_):
    print('Админ следит за чатом!')
        
from test import moderators
moderators()
    
from handlers import client, admin, other, all

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
all.register_handlers_all(dp)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
