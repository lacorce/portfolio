from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def cryptobot_markup() -> types.InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()

     builder.row(types.InlineKeyboardButton(text='Как настроить VPN?', callback_data='oftentimes_ask:2'))

     builder.row(types.InlineKeyboardButton(text='‹', callback_data='back_to_menu'))
     
     return builder.as_markup()