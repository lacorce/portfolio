from aiogram import F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from src.core.routes import user_router
from src.database import xui_configs_api
from ..utils import get_time_word

@user_router.callback_query(F.data.startswith("vpn_detail:"))
async def vpn_detail_handler(callback: types.CallbackQuery):
    uuid = callback.data.split(":")[1]
    configs = await xui_configs_api.get_configs(chat_id=callback.from_user.id)
    selected_config = next((c for c in configs if uuid in c.config_key), None)

    if not selected_config:
        await callback.answer("Ключ не найден.", show_alert=True)
        return

    vpn_link = selected_config.config_key
    current_time = datetime.now().timestamp()
    remaining = selected_config.expires_time - current_time

    if remaining > 0:
        days = int(remaining // 86400)
        hours = int((remaining % 86400) // 3600)
        minutes = int((remaining % 3600) // 60)

        parts = []
        if days:
            parts.append(f"{days} {get_time_word(days, ('день', 'дня', 'дней'))}")
        if hours:
            parts.append(f"{hours} {get_time_word(hours, ('час', 'часа', 'часов'))}")
        if minutes:
            parts.append(f"{minutes} {get_time_word(minutes, ('минута', 'минуты', 'минут'))}")

        time_text = " и ".join(parts)
    else:
        time_text = "⛔ Время действия истекло"

    await callback.message.edit_text(
        text=f"<i>Меню настройки ключа</i>\n\n<code><blockquote>{vpn_link}</blockquote></code>\n"
             f"<blockquote>🗓 Дата окончания: <i><code>{time_text}</code></i></blockquote>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="‹", callback_data="my_vpn")]
            ]
        )
    )
