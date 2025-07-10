from aiogram import F, types
from aiogram.filters import CommandStart

from src.core import user_rou
from .markup import main_user_menu_markup

@user_rou.callback_query(F.data == 'main_menu')
async def commandstart(call : types.CallbackQuery):
    await call.message.edit_text(text=f'Привет, <b>{call.from_user.first_name}</b>.\n'
                      f'Ты попал в <b>Финансовый Telegram-бот</b>.\n'
                      f'Бот помогает <b>вести учет доходов и расходов, анализировать траты, получать отчеты и уведомления!</b>',
                      reply_markup=await main_user_menu_markup())