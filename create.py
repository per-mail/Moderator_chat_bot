from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from filter_chat import IsAdminFilter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
import os


#запуск из config
#import config
#OWNER_ID  = config.OWNER
#BOT_ID = config.BOT
#GROUP_ID = config.GROUP_ID
#bot = Bot(token=config.TOKEN)

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
GROUP_ID = int(os.getenv('GROUPID'))
OWNER_ID = int(os.getenv('OWNERID'))
BOT_ID = int(os.getenv('BOTID'))

dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(IsAdminFilter)


    
conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER,
   block BOOLEAN,
   admin BOOLEAN);
""")




