from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def add_product_admin_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Файл", callback_data="type_file")
            ],
            [
                InlineKeyboardButton(text="Ссылка", callback_data="type_link")
            ],
            [
                InlineKeyboardButton(text="Файл и ссылка", callback_data="type_file_link")
            ]
        ]
    )
    return keyboard