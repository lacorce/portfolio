from aiogram import F, types
from src.core import user_rou
from src.database import get_product_by_id, get_user_balance, deduct_user_balance, record_purchase

@user_rou.callback_query(F.data.startswith("buy_"))
async def buy_product_handler(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    chat_id = call.from_user.id

    product = await get_product_by_id(product_id)
    if not product:
        await call.message.answer("Товар не найден.")
        await call.answer()
        return

    price = product['price']
    balance = await get_user_balance(chat_id)

    if balance < price:
        await call.message.answer("Недостаточно средств на балансе для покупки.")
        await call.answer()
        return

    success = await deduct_user_balance(chat_id, price)
    if not success:
        await call.message.answer("Ошибка при списании баланса.")
        await call.answer()
        return

    await record_purchase(chat_id, product_id, price)

    await call.message.answer(
        f"✅ Покупка успешна!\n"
        f"Товар: <b>{product['name']}</b>\n"
        f"Списано: {price} ₽\n"
        f"Остаток на балансе: {balance - price} ₽"
    )

    if product['file_path']:
        await call.message.answer_document(product['file_path'])
    elif product['link']:
        await call.message.answer(f"Ссылка на товар: {product['link']}")

    await call.answer()
