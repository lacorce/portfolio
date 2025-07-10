from aiogram import F, types

from src.core import user_rou
from .markup import report_periods_markup

@user_rou.callback_query(F.data == 'reports')
async def reports_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Выберите период для отчёта:",
        reply_markup=report_periods_markup()
    )