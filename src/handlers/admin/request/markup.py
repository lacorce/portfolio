from aiogram import types 
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def delete_message() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
            types.InlineKeyboardButton(
                text='❌',
                callback_data='delete_message'
            )
        )
    
    return builder.as_markup()