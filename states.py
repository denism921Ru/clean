from aiogram.fsm.state import StatesGroup, State


class RoleSelect(StatesGroup):
    choosing = State()
