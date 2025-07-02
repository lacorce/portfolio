from aiogram import F, types
from aiogram.fsm.context import FSMContext
from src.core import user_rou
from src.integrations import create_invoice, check_invoice_status, convert_rub_to_usdt
from src.database import add_user_balance
from .fsm import Replenish
from .markup import replenish_user_kb

@user_rou.callback_query(F.data == "replenish_user")
async def start_replenish(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите сумму пополнения:")
    await state.set_state(Replenish.waiting_for_amount)
    await state.update_data(user_id=call.from_user.id)
    await call.answer()

@user_rou.message(Replenish.waiting_for_amount)
async def process_amount(mess: types.Message, state: FSMContext):
    try:
        rub_amount = float(mess.text.strip())
        if rub_amount <= 0:
            raise ValueError
    except ValueError:
        await mess.answer("Введите корректное число.")
        return

    try:
        rub_amount = await convert_rub_to_usdt(rub_amount)
    except Exception as e:
        await mess.answer("Ошибка получения курса валют. Попробуйте позже.")
        return

    invoice_data = await create_invoice(rub_amount)
    if not invoice_data:
        await mess.answer("Ошибка создания счёта. Попробуйте позже.")
        await state.clear()
        return

    invoice_id = invoice_data.get("invoice_id")

    await state.update_data(invoice_id=invoice_id, rub_amount=rub_amount, usdt_amount=rub_amount)

    await mess.answer(
        f"🔄 Счёт создан:\n"
        f"💰 {rub_amount} RUB ≈ <b>{rub_amount} USDT</b>\n\n"
        f"Нажмите кнопку ниже для оплаты:",
        reply_markup=await replenish_user_kb(payment_url=invoice_data.get("pay_url"))
    )
    await state.set_state(Replenish.waiting_for_check)

@user_rou.callback_query(F.data == "check_invoice_status")
async def check_invoice(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    invoice_id = data.get("invoice_id")
    rub_amount = data.get("rub_amount")
    usdt_amount = data.get("usdt_amount")
    user_id = data.get("user_id")

    status_data = await check_invoice_status(invoice_id)
    status = status_data.get("status")

    if status == "paid":
        await add_user_balance(user_id=user_id, amount=usdt_amount)
        await call.message.answer(
            f"✅ Оплата подтверждена!\n"
            f"💳 Баланс пополнен на {rub_amount} RUB ({usdt_amount} USDT)."
        )
        await state.clear()
    else:
        await call.message.answer("Оплата не найдена.")
    await call.answer()

