from aiogram import types 
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def support_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
        types.InlineKeyboardButton(
            text='📚 Часто задаваемые вопросы',
            callback_data='oftentimes_ask'
        )
    ).row(
            types.InlineKeyboardButton(
                text='👩‍💻 ТП',
                url='https://t.me/radjahelper'
            )
        ).row(
            types.InlineKeyboardButton(
                text='‹',
                callback_data='back_to_menu'
            )
        )
    
    return builder.as_markup()
