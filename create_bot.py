from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from filters import IsAdminFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
import os


#запуск из config
#import config
#GROUP_ID = config.GROUP_ID
#ADMIN = config.ADMIN
#bot = Bot(token=config.TOKEN)

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
ADMIN = int(os.getenv('ADMINID'))
GROUP_ID = int(os.getenv('GROUPID'))

dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(IsAdminFilter)


conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER,
   block INTEGER);
""")
conn.commit()
