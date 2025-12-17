from aiogram.fsm.state import StatesGroup, State

class RoleState(StatesGroup):
    choosing_role = State()
