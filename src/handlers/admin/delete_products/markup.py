from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_admin_products_keyboard(products: list[dict]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"❌ Удалить товар: {p['name']}", callback_data=f"del_product:{p['id']}")]
        for p in products
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
