import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(
            text="💰 Open Mini App",
            web_app=types.WebAppInfo(url="https://yourdomain.com/web/index.html")
        )
    )
    await message.answer(
        f"Welcome {message.from_user.first_name} 👋\nEarn by completing tasks!",
        reply_markup=kb
    )

if __name__ == "__main__":
    executor.start_polling(dp)
