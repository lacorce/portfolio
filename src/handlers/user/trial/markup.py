from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

async def trial_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
          types.InlineKeyboardButton(
            text='📚 Инструкция по подключению',
            callback_data='oftentimes_ask:2'
          )   
    )
    
    return builder.as_markup() 