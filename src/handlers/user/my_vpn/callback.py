from aiogram import F, types
from datetime import datetime

from src.core.routes import user_router
from src.database import xui_configs_api
from .markup import my_vpn_markup, back_to_menu
from .utils import get_time_word

@user_router.callback_query(F.data == 'my_vpn')
async def my_vpn_keyboard_handler(callback: types.CallbackQuery):
    configs = await xui_configs_api.get_configs(chat_id=callback.from_user.id)

    if not configs:
        await callback.message.edit_text(
            text="❌ У вас нет активных VPN-протоколов.",
            reply_markup=await my_vpn_markup()
        )
        return

    current_time = datetime.now().timestamp()
    active_configs = [c for c in configs if current_time < c.expires_time]
    expired_configs = [c for c in configs if current_time >= c.expires_time]

    if not active_configs:
        await callback.message.edit_text(
            text="⚙️ <i>Меню VPN</i>",
            reply_markup=await my_vpn_markup(expired_configs=expired_configs)
        )
        return

    if len(active_configs) == 1 and not expired_configs:
        selected_config = active_configs[0]
        vpn_link = selected_config.config_key
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
            text=f"⚙️ <i>Меню VPN</i>\n\n<code><blockquote>{vpn_link}</blockquote></code>\n"
                f"<blockquote>🗓 Дата окончания: <i><code>{time_text}</code></i></blockquote>",
            reply_markup=await back_to_menu()
            )
        
        return


    await callback.message.edit_text(
        text="⚙️ <i>Меню VPN</i>",
        reply_markup=await my_vpn_markup(configs=active_configs, expired_configs=expired_configs)
    )

