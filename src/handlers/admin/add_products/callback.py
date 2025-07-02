from aiogram import F, types
from aiogram.fsm.context import FSMContext
from src.core import admin_rou
from src.database import add_product_to_db
from .markup import add_product_admin_kb
from .fsm import AddProductStates

@admin_rou.callback_query(F.data == "add_product")
async def add_product_start(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите тип товара:", reply_markup=await add_product_admin_kb())
    await state.set_state(AddProductStates.choose_type)
    await call.answer()

@admin_rou.callback_query(F.data.startswith("type_"))
async def product_type_chosen(call: types.CallbackQuery, state: FSMContext):
    chosen = call.data
    await state.update_data(product_type=chosen)
    
    if chosen == "type_file":
        await call.message.answer("Отправьте файл (фото, документ и т.д.)")
        await state.set_state(AddProductStates.waiting_file)
    elif chosen == "type_link":
        await call.message.answer("Отправьте ссылку на товар")
        await state.set_state(AddProductStates.waiting_link)
    elif chosen == "type_file_link":
        await call.message.answer("Отправьте файл (фото, документ и т.д.)")
        await state.set_state(AddProductStates.waiting_file)
    await call.answer()

@admin_rou.message(AddProductStates.waiting_file, F.content_type.in_({'photo', 'document'}))
async def handle_product_file(mess: types.Message, state: FSMContext):
    if mess.photo:
        file_id = mess.photo[-1].file_id
    elif mess.document:
        file_id = mess.document.file_id
    else:
        await mess.answer("Пожалуйста, отправьте корректный файл (фото или документ).")
        return

    await state.update_data(file_id=file_id)
    data = await state.get_data()

    if data.get("product_type") == "type_file_link":
        await mess.answer("Теперь отправьте ссылку на товар.")
        await state.set_state(AddProductStates.waiting_link_file)
    else:
        await mess.answer("Теперь отправьте описание товара.")
        await state.set_state(AddProductStates.waiting_description)

@admin_rou.message(AddProductStates.waiting_link)
@admin_rou.message(AddProductStates.waiting_link_file)
async def handle_product_link(mess: types.Message, state: FSMContext):
    await state.update_data(link=mess.text)

    await mess.answer("Теперь отправьте описание товара.")
    await state.set_state(AddProductStates.waiting_description)

@admin_rou.message(AddProductStates.waiting_description)
async def handle_product_description(mess: types.Message, state: FSMContext):
    await state.update_data(description=mess.text)
    await mess.answer("Теперь отправьте цену товара (только число, без ₽).")
    await state.set_state(AddProductStates.waiting_price)

@admin_rou.message(AddProductStates.waiting_price)
async def handle_product_price(mess: types.Message, state: FSMContext):
    try:
        price = float(mess.text.replace(",", "."))
    except ValueError:
        await mess.answer("Введите корректное число для цены.")
        return

    await state.update_data(price=price)
    data = await state.get_data()

    await add_product_to_db(
        name="Товар",
        description=data.get("description"),
        price=price,
        file_path=data.get("file_id"),
        link=data.get("link")
    )

    await mess.answer("Товар успешно добавлен ✅")
    await state.clear()