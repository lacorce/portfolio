from aiogram.fsm.state import StatesGroup, State

class AddTransactionStates(StatesGroup):
    waiting_for_type = State()
    waiting_for_amount = State()
    waiting_for_currency = State()