from aiogram.dispatcher.filters.state import State, StatesGroup

class ConvertState(StatesGroup):
    waiting_for_amount = State()
