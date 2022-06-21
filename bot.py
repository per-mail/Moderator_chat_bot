from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from Talk import speak
print("BOT")

bot = Bot(token='5060714683:AAESVO_6E6YT_RHhpFMXuCWnmpRFV6LsO7c')

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler()
async def echo_message(message: types.Message):
    reply = speak(message.text)
    await message.reply(reply)
    



    
    


if __name__ == '__main__':
    executor.start_polling(dp)
