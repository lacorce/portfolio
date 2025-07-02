from aiogram import F, types
from aiogram.filters import CommandStart
from src.core import user_rou, open_config
from .markup import main_user_kb
from src.database import get_user_balance
from src.handlers.admin.markup import main_admin_kb

@user_rou.message(CommandStart())
async def command_start(mess : types.Message):
    if mess.from_user.id == open_config('owner_id'):
        await mess.answer(f'Администратор <b>{mess.from_user.first_name}</b>, привет.\n\n'
                        'Общий доход: \n'
                        'Количество покупок: \n'
                        'Кол-во пользователей: '
                        ,reply_markup=await main_admin_kb())
    else:
        await mess.answer(text=f'Привет, <b>{mess.from_user.first_name}</b>.\n'
                    f'Ваш баланс: <code>{await get_user_balance(mess.from_user.id)}₽</code>'
                    ,reply_markup=await main_user_kb())