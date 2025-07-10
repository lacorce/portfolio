from aiogram import F, types
from aiogram.fsm.context import FSMContext

from src.core import user_rou
from src.database import transactions_dal
from .fsm import AddTransactionStates
from .markup import select_currencies_markup

@user_rou.callback_query(AddTransactionStates.waiting_for_type, F.data.startswith("transaction_type_"))
async def process_transaction_type(call: types.CallbackQuery, state: FSMContext):
    tx_type = call.data.split("_")[-1]

    await state.update_data(transaction_type=tx_type)
    await call.message.edit_text(f"Вы выбрали: {'Доход' if tx_type == 'income' else 'Трата'}.\nВведите сумму транзакции:")
    await state.set_state(AddTransactionStates.waiting_for_amount)

@user_rou.message(AddTransactionStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите корректное число для суммы.')
        return

    await state.update_data(amount=int(message.text))

    await message.answer("Выберите валюту транзакции:", reply_markup=await select_currencies_markup())
    await state.set_state(AddTransactionStates.waiting_for_currency)

@user_rou.callback_query(AddTransactionStates.waiting_for_currency, F.data.startswith("currency_"))
async def process_currency_callback(call: types.CallbackQuery, state: FSMContext):
    currency = call.data.split("_")[1]
    await state.update_data(currency=currency)
    data = await state.get_data()

    from datetime import datetime
    created_at = int(datetime.utcnow().timestamp())

    await transactions_dal.add_transaction(
        chat_id=call.from_user.id,
        type_=data["transaction_type"],\
        amount=data["amount"],
        currency=currency,
        created_at=created_at
    )

    await call.message.edit_text(
        f"✅ Транзакция добавлена:\n"
        f"Тип: {'Доход' if data['transaction_type'] == 'income' else 'Трата'}\n"
        f"Сумма: {data['amount']}\n"
        f"Валюта: {currency}"
    )
    
    await state.clear()
