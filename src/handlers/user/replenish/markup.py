from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def replenish_user_kb(payment_url):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 Оплатить", url=payment_url)
            ],
            [
                InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_invoice_status")
            ]
        ]
    )
    return keyboard