from aiogram.fsm.state import StatesGroup, State

class AddProductStates(StatesGroup):
    choose_type = State()
    waiting_file = State()
    waiting_link = State()
    waiting_link_file = State()
    waiting_description = State()
    waiting_price = State()
