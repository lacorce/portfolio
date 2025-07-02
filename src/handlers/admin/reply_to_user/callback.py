from aiogram import F, types
from aiogram.fsm.context import FSMContext
from src.core import admin_rou
from .fsm import SupportStates

@admin_rou.callback_query(F.data.startswith("owner_reply_"))
async def owner_start_reply(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split("_")[-1])
    await state.set_state(SupportStates.waiting_for_owner_reply)
    await state.update_data(reply_to_user=user_id)
    await call.message.answer(f"Напишите ответ пользователю {user_id}:")
    await call.answer()

@admin_rou.message(SupportStates.waiting_for_owner_reply)
async def owner_send_reply(mess: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("reply_to_user")
    reply_text = mess.text

    await mess.bot.send_message(user_id, f"Ответ поддержки:\n\n{reply_text}")
    await mess.answer("Ответ отправлен пользователю.")


    await state.clear()