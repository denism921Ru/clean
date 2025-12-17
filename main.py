import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from states import RoleSelect

# временное хранилище ролей (позже заменим на БД)
USERS = {}  # user_id -> role

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states import RoleState
def role_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👷‍♀️ Я горничная")],
            [KeyboardButton(text="🧑‍💼 Я администратор")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Назначить уборку")],
            [KeyboardButton(text="👷‍♀️ Мои горничные")],
            [KeyboardButton(text="📋 Мои уборки")]
        ],
        resize_keyboard=True
    )


def cleaner_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Начать смену")],
            [KeyboardButton(text="📋 Мои заявки")]
        ],
        resize_keyboard=True
    )


async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id in USERS:
        role = USERS[user_id]
        if role == "admin":
            await message.answer("Вы вошли как администратор", reply_markup=admin_menu())
        else:
            await message.answer("Вы вошли как горничная", reply_markup=cleaner_menu())
        return

    await message.answer(
        "Добро пожаловать 👋\nКто вы?",
        reply_markup=role_keyboard()
    )
    await state.set_state(RoleSelect.choosing)


async def role_chosen(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text

    if "администратор" in text.lower():
        USERS[user_id] = "admin"
        await message.answer(
            "✅ Роль установлена: Администратор",
            reply_markup=admin_menu()
        )

    elif "горничная" in text.lower():
        USERS[user_id] = "cleaner"
        await message.answer(
            "✅ Роль установлена: Горничная",
            reply_markup=cleaner_menu()
        )
    else:
        await message.answer("Пожалуйста, выберите роль кнопкой")
        return

    await state.clear()


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())
    dp.message.register(role_chosen, RoleSelect.choosing)

    print("✅ Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
