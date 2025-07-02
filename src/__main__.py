import asyncio

from aiogram import Dispatcher
from src.core import bot, setup_logger
from src.handlers import user_rou, admin_rou
from src.database import init_db

async def start_bot():
    dp = Dispatcher()
    await init_db()
    setup_logger()
    dp.include_routers(user_rou, admin_rou)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())