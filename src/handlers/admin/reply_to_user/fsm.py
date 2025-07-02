from aiogram.fsm.state import StatesGroup, State

class SupportStates(StatesGroup):
    waiting_for_owner_reply = State()