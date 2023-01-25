from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin(StatesGroup):
    home = State()
    edit = State()



