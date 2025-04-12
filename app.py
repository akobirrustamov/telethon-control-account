import asyncio

from aiogram import executor

from handlers.users.echo import send_random_messages
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


from environs import Env

env = Env()
env.read_env()  # Load environment variables from .env


async def on_startup(dispatcher):



    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

     # Wait for 2 minutes
    # await scheduler()
# async def scheduler():
#     while True:
#         await send_random_messages()
#         await asyncio.sleep(20)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
