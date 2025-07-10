from aiogram import F, types
from aiogram.utils.markdown import hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core import user_rou
from src.database import transactions_dal

from datetime import datetime

@user_rou.callback_query(F.data == 'finances')
async def finances_handler(call: types.CallbackQuery):
    chat_id = call.from_user.id

    transactions = await transactions_dal.get_transactions(chat_id=chat_id)

    if not transactions:
        await call.message.edit_text("У вас нет финансовых операций.")
        return

    balances = {}

    income_types = ["income", "доход", "popolnenie"]
    expense_types = ["expense", "трата", "rashod"]

    for tx in transactions:
        currency = tx.currency.upper()
        if currency not in balances:
            balances[currency] = 0

        if tx.type in income_types:
            balances[currency] += tx.amount
        elif tx.type in expense_types:
            balances[currency] -= tx.amount

    text = f"{hbold('💰 Ваш баланс:')}\n"
    for cur, amount in balances.items():
        text += f"{amount} {cur}\n"

    text += f"\n{hbold('📄 Транзакции:')} ({len(transactions)} шт)\n\n"

    keyboard_buttons = []

    for tx in transactions:
        tx_type_emoji = "🔼" if tx.type in income_types else "🔽"
        amount = f"{tx.amount} {tx.currency.upper()}"
        date = datetime.fromtimestamp(tx.created_at).strftime("%d.%m.%Y %H:%M")
        text += f"{tx_type_emoji} {amount} — {date}\n"

        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"{tx_type_emoji} {amount}",
                callback_data="noop"
            )
        ])

    keyboard_buttons.append([
        InlineKeyboardButton(
            text="Назад",
            callback_data="main_menu"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await call.message.edit_text(text=text, reply_markup=keyboard)
