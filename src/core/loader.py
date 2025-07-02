from aiogram import Bot
from src.core import open_config
from aiogram.client.bot import DefaultBotProperties

bot = Bot(
    token=open_config("token"),
    default=DefaultBotProperties(parse_mode="HTML")
)