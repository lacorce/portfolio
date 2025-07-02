from aiogram import F, types
from src.core import user_rou
from src.database import get_user_purchases

@user_rou.callback_query(F.data == "purchases_user")
async def show_user_purchases(call: types.CallbackQuery):
    purchases = await get_user_purchases(call.from_user.id)
    if not purchases:
        await call.message.answer("У вас пока нет покупок.")
    else:
        text = "📦 Ваши покупки:\n\n"
        for name, amount, status, created_at in purchases:
            text += (f"• <b>{name}</b>\n"
                     f"  Сумма: {amount} USDT\n"
                     f"  Статус: {status}\n"
                     f"  Дата: {created_at}\n\n")

        await call.message.answer(text=text)
        
    await call.answer()