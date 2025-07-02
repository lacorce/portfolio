from aiogram import types, F
from aiogram.fsm.context import FSMContext
from .fsm import SupportStates
from src.core import user_rou, open_config
from .markup import reply_to_user_kb

@user_rou.callback_query(F.data == "supporting_user")
async def ask_user_message(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Опишите вашу проблему или вопрос:")
    await state.set_state(SupportStates.waiting_for_user_message)
    await state.update_data(chat_id=call.from_user.id)
    await call.answer()

@user_rou.message(SupportStates.waiting_for_user_message)
async def receive_user_message(mess: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data.get("chat_id")
    user_msg = mess.text

    await mess.bot.send_message(
        open_config('owner_id'),
        f"Сообщение от пользователя {chat_id}:\n\n{user_msg}",
        reply_markup=await reply_to_user_kb(chat_id=mess.from_user.id)
    )
    await mess.answer("Ваше сообщение отправлено в поддержку, ожидайте ответа.")
    await state.clear()