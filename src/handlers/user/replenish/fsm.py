from aiogram.fsm.state import State, StatesGroup

class Replenish(StatesGroup):
    waiting_for_amount = State()
    waiting_for_check = State()