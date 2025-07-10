from src.core.config import settings

from aiogram import types 
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def subscribe_markup(bot_username: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
        types.InlineKeyboardButton(
            text='📨 Новостной канал',
            url=f'{settings.news_channel_url}'
        )
    ).row(
        types.InlineKeyboardButton(
            text='Проверить подписку 🔄',
            url=f'https://t.me/{bot_username}?start=0'
        )
    )
    
    return builder.as_markup()
