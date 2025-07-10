from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def payment_markup(url: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

  
    builder.row(
        types.InlineKeyboardButton(
            text='🧾 Оплатить',
            url=url
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text='👩‍💻 ТП',
            url='https://t.me/radjahelper'
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu_state_clear'
        )
    )

    return builder.as_markup()

async def stars_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Оплатить", pay=True)],
            [InlineKeyboardButton(text="👩‍💻 ТП", url='https://t.me/radjahelper')],
            [InlineKeyboardButton(text="«", callback_data="back_to_menu_state_star_clear")]
        ]
    )
