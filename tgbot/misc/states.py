from aiogram.dispatcher.filters.state import State, StatesGroup


class UserFSM(StatesGroup):
    home = State()
    primary_manual = State()
    secondary_manual = State()
    value = State()



