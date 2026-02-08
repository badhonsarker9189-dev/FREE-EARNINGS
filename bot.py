import logging
import sqlite3
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

API_URL = "http://localhost:5000"   # Railway হলে পরে change করবে

# ---------------- USER START ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name

    # register user
    try:
        requests.post(f"{API_URL}/register", json={
            "id": user_id,
            "name": name
        })
    except:
        pass

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(
            text="💎 Open Earn App",
            web_app=types.WebAppInfo(
                url="https://YOUR-RAILWAY-URL/web/index.html"
            )
        )
    )

    await message.answer(
        f"👋 Welcome {name}\n\n"
        "💰 Earn money by completing tasks\n"
        "💸 Minimum withdraw: ৳500",
        reply_markup=kb
    )

# ---------------- ADMIN COMMANDS ----------------
def admin_only(message):
    return message.from_user.id == ADMIN_ID

@dp.message_handler(commands=["pending_tasks"])
async def pending_tasks(message: types.Message):
    if not admin_only(message): return

    r = requests.get(f"{API_URL}/admin/pending-tasks").json()
    if not r:
        await message.answer("No pending tasks")
        return

    for x in r:
        await message.answer(
            f"🆔 Task ID: {x[0]}\n"
            f"👤 User: {x[1]}\n"
            f"📌 Task: {x[2]}\n"
            f"💰 Reward: ৳{x[3]}\n\n"
            f"/approve_task {x[0]}"
        )

@dp.message_handler(commands=["approve_task"])
async def approve_task(message: types.Message):
    if not admin_only(message): return
    try:
        tid = message.text.split()[1]
        requests.get(f"{API_URL}/admin/approve-task/{tid}")
        await message.answer("✅ Task Approved")
    except:
        await message.answer("❌ Error")

@dp.message_handler(commands=["pending_withdraw"])
async def pending_withdraw(message: types.Message):
    if not admin_only(message): return

    r = requests.get(f"{API_URL}/admin/pending-withdraw").json()
    if not r:
        await message.answer("No pending withdraw")
        return

    for x in r:
        await message.answer(
            f"🆔 Withdraw ID: {x[0]}\n"
            f"👤 User: {x[1]}\n"
            f"💸 Amount: ৳{x[2]}\n"
            f"📲 {x[3]}: {x[4]}\n\n"
            f"/approve_withdraw {x[0]}"
        )

@dp.message_handler(commands=["approve_withdraw"])
async def approve_withdraw(message: types.Message):
    if not admin_only(message): return
    try:
        wid = message.text.split()[1]
        requests.get(f"{API_URL}/admin/approve-withdraw/{wid}")
        await message.answer("💸 Withdraw Paid")
    except:
        await message.answer("❌ Error")

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)@dp.message_handler(commands=["pending_tasks"])
async def pending_tasks(message: types.Message):
    if message.from_user.id!=ADMIN_ID: return
    import requests
    r=requests.get("http://localhost:5000/admin/pending-tasks").json()
    for x in r:
        await message.answer(
        f"ID:{x[0]}\nUser:{x[1]}\nTask:{x[2]}\n৳{x[3]}\n/approve_task {x[0]}"
        )

@dp.message_handler(commands=["approve_task"])
async def approve_task_cmd(message: types.Message):
    if message.from_user.id!=ADMIN_ID: return
    id=message.text.split()[1]
    import requests
    requests.get(f"http://localhost:5000/admin/approve-task/{id}")
    await message.answer("✅ Approved")

@dp.message_handler(commands=["pending_withdraw"])
async def pending_w(message: types.Message):
    if message.from_user.id!=ADMIN_ID: return
    import requests
    r=requests.get("http://localhost:5000/admin/pending-withdraw").json()
    for x in r:
        await message.answer(
        f"ID:{x[0]}\nUser:{x[1]}\n৳{x[2]}\n{x[3]}:{x[4]}\n/approve_withdraw {x[0]}"
        )

@dp.message_handler(commands=["approve_withdraw"])
async def approve_w(message: types.Message):
    if message.from_user.id!=ADMIN_ID: return
    id=message.text.split()[1]
    import requests
    requests.get(f"http://localhost:5000/admin/approve-withdraw/{id}")
    await message.answer("💸 Paid")
