from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def report_periods_markup():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="За день", callback_data="report_period_day"),
            InlineKeyboardButton(text="За неделю", callback_data="report_period_week"),
            InlineKeyboardButton(text="За месяц", callback_data="report_period_month"),
        ]
    ])
    return keyboard