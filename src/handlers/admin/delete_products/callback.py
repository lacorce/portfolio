from aiogram import F, types
from src.core import admin_rou
from src.database import get_all_products, delete_product_from_db
from .markup import generate_admin_products_keyboard

@admin_rou.callback_query(F.data == "del_product")
async def admin_show_products(call: types.CallbackQuery):
    products = await get_all_products()
    if not products:
        return
    kb = generate_admin_products_keyboard(products)
    await call.message.answer("Список товаров :", reply_markup=kb)

@admin_rou.callback_query(F.data.startswith("del_product:"))
async def handle_delete_product(call: types.CallbackQuery):
    product_id = int(call.data.split(":")[1])
    await delete_product_from_db(product_id)
    await call.answer("Товар удалён!")
    await call.message.delete()