from aiogram.fsm.state import StatesGroup, State


class CleaningStates(StatesGroup):
    start_shift = State()
    select_task = State()
    start_cleaning = State()
    checklist = State()
    finish_cleaning = State()
