from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):

    name = State()
    phone = State()