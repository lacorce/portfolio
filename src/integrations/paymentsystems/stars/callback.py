from aiogram.types import Message
# from aiogram.filters import SuccessfulPaymentFilter
from src.core.routes import user_router

# @user_router.message(SuccessfulPaymentFilter())
# async def handle_successful_stars_payment(message: Message):
#     user_id = message.from_user.id
#     username = message.from_user.username
#     amount = message.successful_payment.total_amount 
#     currency = message.successful_payment.currency
#     payload = message.successful_payment.invoice_payload

#     print(f"Пользователь {user_id} (@{username}) оплатил {amount} {currency} через Stars. Payload: {payload}")

#     await message.answer(
#         f"✅ Спасибо за оплату!\n"
#         f"💰 Сумма: {amount} {currency}\n"
#         f"🧾 Payload: <code>{payload}</code>"
#     )
