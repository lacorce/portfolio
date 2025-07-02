from aiogram.fsm.state import StatesGroup, State

class SupportStates(StatesGroup):
    waiting_for_user_message = State()