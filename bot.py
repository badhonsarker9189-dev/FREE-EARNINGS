import logging, sqlite3
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Start command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users(id, name, balance) VALUES (?, ?, ?)", (user_id, name, 0))
    conn.commit()
    conn.close()

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(
        text="💰 Open Mini App",
        web_app=types.WebAppInfo(url="https://yourdomain.com/web/index.html")
    ))
    await message.answer(f"Welcome {name} 👋", reply_markup=kb)

# Admin command
@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("🚫 You are not admin")
        return
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📊 View Stats"))
    await message.answer("Admin Panel", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp)
