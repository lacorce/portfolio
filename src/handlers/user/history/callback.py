from aiogram import F, types
from src.core.routes import user_router
from .markup import history_markup, back_markup

@user_router.callback_query(F.data == 'history')
async def history_callback_query_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Действительные и просроченные ключи
    valid_keys = ["Ключ-1 — до 10.05.2025"]
    expired_keys = ["Ключ-1 — до 10.05.2025"]

    # Активные и использованные купоны
    active_coupons = ["Купон-5% — 20.02.2025"]
    used_coupons = ["Купон-5% — 20.02.2025"]

    # Флаги наличия данных
    has_valid_keys = bool(valid_keys)
    has_expired_keys = bool(expired_keys)
    has_active_coupons = bool(active_coupons)
    has_used_coupons = bool(used_coupons)

    has_keys = has_valid_keys or has_expired_keys
    has_coupons = has_active_coupons or has_used_coupons

    # Проверяем условие (1 ключ + 1 купон из разных категорий)
    one_key_one_coupon = (has_valid_keys and has_used_coupons) or (has_expired_keys and has_active_coupons)

    # Начальный текст
    text = "🗂 <i>Меню истории</i>"

    if not one_key_one_coupon:  # Если больше данных, добавляем их в текст
        if has_valid_keys:
            text += "\n\n🔑 <b>Действительные ключи:</b>\n" + "\n".join(valid_keys)
        if has_expired_keys:
            text += "\n\n⛔ <b>Просроченные ключи:</b>\n" + "\n".join(expired_keys)

        if has_active_coupons:
            text += "\n\n🪪 <b>Активные купоны:</b>\n" + "\n".join(active_coupons)
        if has_used_coupons:
            text += "\n\n♻ <b>Использованные купоны:</b>\n" + "\n".join(used_coupons)

    # Выбор клавиатуры
    markup = await history_markup(has_keys, has_coupons) if one_key_one_coupon else await back_markup()

    await callback.message.edit_text(
        text=text,
        reply_markup=markup
    )
