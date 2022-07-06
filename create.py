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

#указали хранилище состояний в оперативной памяти, так как потеря этих состояний
#нам не страшна (да и этот вариант больше всего подходит для демонстрационных целей,
#так как не требует настройки).
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
GROUP_ID = int(os.getenv('GROUPID'))
OWNER_ID = int(os.getenv('OWNERID'))
BOT_ID = int(os.getenv('BOTID'))

dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(IsAdminFilter)
#dp.filters_factory.bind(AdminFilter)

#создание базы обычное    
#conn = sqlite3.connect('db.db')
#cur = conn.cursor()
#cur.execute("""CREATE TABLE IF NOT EXISTS users(
#   user_id INTEGER,
#   block BOOLEAN,
#   admin BOOLEAN);
#""")

#создание базы с autocommit
conn = sqlite3.connect('db.db')
# эта строка включает autocommit
conn.isolation_level = None

with conn:
    try:
        cur = conn.execute ("""CREATE TABLE IF NOT EXISTS users(
                            user_id INTEGER,
                            block BOOLEAN,
                            admin BOOLEAN);
""")
    except sqlite3.Error as e:
        print(Error)


