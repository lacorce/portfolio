from aiogram import types 
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def back_refferal() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
            types.InlineKeyboardButton(
                text='‹',
                callback_data='refferal'
            )
        )
    
    return builder.as_markup()


async def request_to_admin_keyboard(chat_id: int, lvl: int, id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(
            text='➕',
            callback_data=f'requestpriz_{chat_id}_{lvl}_{id}_yes'
        ),
        types.InlineKeyboardButton(
            text='➖',
            callback_data=f'requestpriz_{chat_id}_{lvl}_{id}_no'
        )
    )

    return builder.as_markup()