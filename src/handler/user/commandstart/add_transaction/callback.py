from aiogram import F, types
from aiogram.fsm.context import FSMContext

from src.core import user_rou
from .fsm import AddTransactionStates
from .markup import select_transaction_type_markup

@user_rou.callback_query(F.data == 'add_transaction')
async def add_transaction_handler(call: types.CallbackQuery, state: FSMContext):

    await call.message.edit_text(
        text='Выберите тип транзакции:',
        reply_markup=await select_transaction_type_markup()
    )
    await state.set_state(AddTransactionStates.waiting_for_type)