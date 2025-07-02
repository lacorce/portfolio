from aiogram import F, types
from src.core import user_rou
from src.database import get_all_products, get_product_by_id
from typing import List, Dict
from .markup import generate_products_keyboard, buy_kb

def paginate_products(products: List[Dict], page: int, page_size: int = 5) -> List[Dict]:
    start = page * page_size
    end = start + page_size
    return products[start:end]

@user_rou.callback_query(F.data == 'catalog_user')
async def catalog_user_keyboard_handler(call: types.CallbackQuery):
    all_products = await get_all_products()
    if not all_products:
        await call.message.answer("Товары не найдены.")
        await call.answer()
        return

    page = 0
    products_page = paginate_products(all_products, page)
    kb = generate_products_keyboard(products_page, page, len(all_products))
    await call.message.answer("Каталог товаров:", reply_markup=kb)
    await call.answer()

@user_rou.callback_query(F.data.startswith("catalog_page_"))
async def catalog_pagination_handler(call: types.CallbackQuery):
    all_products = await get_all_products()
    page = int(call.data.split("_")[-1])
    products_page = paginate_products(all_products, page)
    kb = generate_products_keyboard(products_page, page, len(all_products))
    await call.message.edit_reply_markup(reply_markup=kb)
    await call.answer()

@user_rou.callback_query(F.data.startswith("product_"))
async def product_callback_handler(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    product = await get_product_by_id(product_id)

    if not product:
        await call.message.answer("Товар не найден.")
        await call.answer()
        return

    text = (
        f"🛍️ <b>Название:</b> {product['name']}\n"
        f"📝 <b>Описание:</b> {product['description'] or '— отсутствует'}\n"
        f"💰 <b>Цена:</b> <code>{product['price']}₽</code>"
    )

    await call.message.answer(text=text, reply_markup=await buy_kb(product_id))
    await call.answer()
