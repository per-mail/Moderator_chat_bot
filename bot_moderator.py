import logging
from aiogram.utils import executor

from create_bot import dp

# log
logging.basicConfig(level=logging.INFO)

# функция оповещение о старте
async def on_startup(_):
    print('Админ следит за чатом!')

from handlers import client, admin, other, all

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
all.register_handlers_all(dp)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
