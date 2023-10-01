from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import aioschedule
import asyncio

bot = Bot(token="6507738477:AAGYbbfS739p7LMJ_eTZk--mCpKdAAOC3CI")
dp = Dispatcher(bot)

def new_user(uid):
    with open("users.txt", "a") as f:
        f.write(str(uid) + "\n")

def get_users_list():
    with open("users.txt", "r") as f:
        return f.readlines()

async def start_mailing():  
    for i in get_users_list():
        try:
            await bot.send_message(chat_id=i, text="Это рассылка")
        except:
            pass

async def scheduler():
    aioschedule.every().day.do(start_mailing)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(dp):
    asyncio.create_task(scheduler())

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Привет! Тут ты будешь получать рассылку.")
    new_user(user_id)

@dp.message_handler(commands=["mailing"])
async def mailing(message: types.Message):
    user_id = message.from_user.id
    if user_id == YOUR_ADMIN_USER_ID:  
        await start_mailing()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
