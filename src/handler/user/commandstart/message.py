from aiogram import F, types
from aiogram.filters import CommandStart

from src.core import user_rou
from .markup import main_user_menu_markup

@user_rou.message(CommandStart())
async def commandstart(mess : types.Message):
    await mess.answer(f'Привет, <b>{mess.from_user.first_name}</b>.\n'
                      f'Ты попал в <b>Финансовый Telegram-бот</b>.\n'
                      f'Бот помогает <b>вести учет доходов и расходов, анализировать траты.</b>',
                      reply_markup=await main_user_menu_markup())