from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_course_period(payment_method: int) -> str:
    courses = {
        'yookassa': '₽',
        'cryptobot': '$',
        'stars': '🌟'
    }
    return courses[payment_method]


async def period_markup(protocol: str,
                        payment_method: int,
                        amount_keys: int,
                        start_amount: float) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    course = get_course_period(payment_method=payment_method)

    months_list = [1, 2, 3, 6, 12]

    for months in months_list:
        amount = round(months * float(start_amount), 2)
        formatted_amount = int(amount) if amount.is_integer() else amount

        builder.row(
            types.InlineKeyboardButton(
                text = f'⏳ {months} месяц{"а" if 2 <= months <= 4 else ""}{"ев" if months >= 5 else ""} — {formatted_amount} {course}',
                callback_data=f'sending:{protocol}:{payment_method}:{amount_keys}:{formatted_amount}:{months}',
            ),
        )

    builder.row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data=f'payment_method:{protocol}:{payment_method}'
        ),
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu'
        )
    )

    return builder.as_markup()
