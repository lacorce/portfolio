import asyncio
import uvicorn
from fastapi import FastAPI
from src.core import bot, setup_logger
from src.database import db
from aiogram import Dispatcher
from src.handlers import user_router
from src.integrations import yookassa_router
from src.scheduler import start_scheduler

app = FastAPI()

app.include_router(yookassa_router)

async def on_startup():
    await db.init_models()
    await start_scheduler()

async def start_bot():
    dp = Dispatcher()
    dp.include_routers(user_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    setup_logger()

    await on_startup()

    tasks = [
        asyncio.create_task(start_bot()),
        asyncio.create_task(start_fastapi()),
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())