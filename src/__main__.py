import asyncio

from aiogram import Dispatcher
from .core import bot, setup_logger
from .handler import user_rou
from .database import db

async def start_bot():
    setup_logger()
    await db.init_models()
    dp = Dispatcher()
    dp.include_routers(user_rou)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())