import logging
from aiogram.utils import executor

from create import dp

#делаем импорт из фильтра adm_filter здесь, чтобы не было зацикливания
from adm_filter import AdminFilter
dp.filters_factory.bind(AdminFilter)


# log
logging.basicConfig(level=logging.INFO)

# функция оповещение о старте
async def on_startup(_):
    print('Админ следит за чатом!')     
   
from handlers import start, admin, other, empty

start.register_handlers_start(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
empty.register_handlers_empty(dp)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
