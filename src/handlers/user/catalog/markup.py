from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_products_keyboard(products: list, page: int, total_count: int, page_size: int = 5) -> InlineKeyboardMarkup:
    buttons = []
    for product in products:
        buttons.append([InlineKeyboardButton(text=product['name'], callback_data=f"product_{product['id']}")])

    total_pages = (total_count - 1) // page_size
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("<-", callback_data=f"catalog_page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("->", callback_data=f"catalog_page_{page+1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def buy_kb(product_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛒 Купить", callback_data=f"buy_{product_id}")
            ]
        ]
    )
    return keyboard
