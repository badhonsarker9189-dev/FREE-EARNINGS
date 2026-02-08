import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# 🔴 Railway deploy করার পর এখানে API URL বসাবে
API_URL = "https://YOUR-RAILWAY-APP.up.railway.app"

# ---------------- START + REFERRAL ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name

    ref = None
    args = message.get_args()
    if args.isdigit():
        ref = int(args)

    # register user
    try:
        requests.post(f"{API_URL}/register", json={
            "id": user_id,
            "name": name,
            "ref": ref
        })
    except:
        pass

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(
            text="💎 Open Earn App",
            web_app=types.WebAppInfo(
                url=f"{API_URL}/web/index.html"
            )
        )
    )

    await message.answer(
        f"👋 Welcome {name}\n\n"
        f"💰 Tasks kore income korun\n"
        f"🎁 Referral bonus: ৳5\n"
        f"💸 Minimum withdraw: ৳500\n\n"
        f"🔗 Your referral link:\n"
        f"https://t.me/{(await bot.get_me()).username}?start={user_id}",
        reply_markup=kb
    )

# ---------------- ADMIN CHECK ----------------
def is_admin(message):
    return message.from_user.id == ADMIN_ID

# ---------------- PENDING TASKS ----------------
@dp.message_handler(commands=["pending_tasks"])
async def pending_tasks(message: types.Message):
    if not is_admin(message):
        return

    r = requests.get(f"{API_URL}/admin/pending-tasks").json()
    if not r:
        await message.answer("✅ No pending tasks")
        return

    for x in r:
        await message.answer(
            f"🆔 Task ID: {x[0]}\n"
            f"👤 User: {x[1]}\n"
            f"📌 Task: {x[2]}\n"
            f"💰 Reward: ৳{x[3]}\n\n"
            f"/approve_task {x[0]}"
        )

# ---------------- APPROVE TASK ----------------
@dp.message_handler(commands=["approve_task"])
async def approve_task(message: types.Message):
    if not is_admin(message):
        return
    try:
        tid = message.text.split()[1]
        requests.get(f"{API_URL}/admin/approve-task/{tid}")
        await message.answer("✅ Task approved")
    except:
        await message.answer("❌ Error approving task")

# ---------------- PENDING WITHDRAW ----------------
@dp.message_handler(commands=["pending_withdraw"])
async def pending_withdraw(message: types.Message):
    if not is_admin(message):
        return

    r = requests.get(f"{API_URL}/admin/pending-withdraw").json()
    if not r:
        await message.answer("✅ No pending withdraw")
        return

    for x in r:
        await message.answer(
            f"🆔 Withdraw ID: {x[0]}\n"
            f"👤 User: {x[1]}\n"
            f"💸 Amount: ৳{x[2]}\n"
            f"📲 {x[3]} : {x[4]}\n\n"
            f"/approve_withdraw {x[0]}"
        )

# ---------------- APPROVE WITHDRAW ----------------
@dp.message_handler(commands=["approve_withdraw"])
async def approve_withdraw(message: types.Message):
    if not is_admin(message):
        return
    try:
        wid = message.text.split()[1]
        requests.get(f"{API_URL}/admin/approve-withdraw/{wid}")
        await message.answer("💸 Withdraw marked as PAID")
    except:
        await message.answer("❌ Error approving withdraw")

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
