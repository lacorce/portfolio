from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def reply_to_user_kb(chat_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ответить", callback_data=f"owner_reply_{chat_id}")
            ]
        ]
    )
    return keyboard