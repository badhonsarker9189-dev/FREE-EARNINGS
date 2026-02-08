@dp.message_handler(commands=["pending_tasks"])
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
