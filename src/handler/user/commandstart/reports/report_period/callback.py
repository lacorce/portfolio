from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from datetime import datetime, timedelta
import os

from src.core import user_rou
from src.database import transactions_dal
from .generator import create_report_chart

async def get_report_stats(user_id: int, start_date: datetime, end_date: datetime) -> dict:
    rows = await transactions_dal.get_transactions_by_period(user_id, int(start_date.timestamp()), int(end_date.timestamp()))
    
    stats = {
        "income": {},
        "expense": {}
    }

    for row in rows:
        t_type = row.type
        category = getattr(row, "category", "Без категории")
        currency = getattr(row, "currency", "USD")
        amount = row.amount

        if t_type == "income":
            if currency not in stats["income"]:
                stats["income"][currency] = {}
            stats["income"][currency][category] = stats["income"][currency].get(category, 0) + amount
        else:
            if currency not in stats["expense"]:
                stats["expense"][currency] = {}
            stats["expense"][currency][category] = stats["expense"][currency].get(category, 0) + amount

    return stats

@user_rou.callback_query(F.data.startswith("report_period_"))
async def report_period_handler(call: types.CallbackQuery, state: FSMContext):
    period = call.data.split("_")[-1]

    now = datetime.utcnow()
    if period == "day":
        start_date = now - timedelta(days=1)
    elif period == "week":
        start_date = now - timedelta(weeks=1)
    elif period == "month":
        start_date = now - timedelta(days=30)
    else:
        await call.answer("Неизвестный период")
        return

    await state.update_data(report_start=start_date.timestamp())
    await state.update_data(report_end=now.timestamp())

    stats = await get_report_stats(call.from_user.id, start_date, now)

    img_path = create_report_chart(stats)

    if not os.path.isfile(img_path):
        await call.message.answer("Ошибка: файл отчёта не найден.")
        return

    text = "📊 Отчет за период:\n\n"
    text += "Доходы:\n"
    if stats["income"]:
        for currency, categories in stats["income"].items():
            text += f"Валюта {currency}:\n"
            for category, amount in categories.items():
                text += f"  {category}: {amount}\n"
    else:
        text += "  Нет данных\n"

    text += "\nРасходы:\n"
    if stats["expense"]:
        for currency, categories in stats["expense"].items():
            text += f"Валюта {currency}:\n"
            for category, amount in categories.items():
                text += f"  {category}: {amount}\n"
    else:
        text += "  Нет данных\n"

    photo = FSInputFile(img_path)
    await call.message.answer_photo(photo=photo, caption=text)
    await call.answer()
