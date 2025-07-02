from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def main_user_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📚 Каталог", callback_data="catalog_user")
            ],
            [
                InlineKeyboardButton(text="💼 Мои покупки", callback_data="purchases_user")
            ],
            [
                InlineKeyboardButton(text="💳 Пополнить", callback_data="replenish_user")
            ],
            [
                InlineKeyboardButton(text="👨‍💼 Поддержка", callback_data="supporting_user")
            ]
        ]
    )
    return keyboard