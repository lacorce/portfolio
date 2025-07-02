from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def main_admin_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Добавить товар", callback_data="add_product")
            ],
            [
                InlineKeyboardButton(text="❌ Удалить товар", callback_data="del_product")
            ]
        ]
    )
    return keyboard