from .config import settings

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))