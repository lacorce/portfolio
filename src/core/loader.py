from .config import open_config

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


bot = Bot(token=open_config('token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))