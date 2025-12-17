import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from states import RoleState

# -------------------------
# ВРЕМЕННОЕ ХРАНИЛИЩЕ РОЛЕЙ
# user_id: "admin" | "housekeeper"
# -------------------------
USER_ROLES = {}


# -------------------------
# КЛАВИАТУРЫ
# -------------------------
def role_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👩‍🧹 Я горничная")],
            [KeyboardButton(text="🧑‍💼 Я администратор")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Назначить уборку")],
            [KeyboardButton(text="👩‍🧹 Мои горничные")],
            [KeyboardButton(text="📋 Мои уборки")]
        ],
        resize_keyboard=True
    )


def housekeeper_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Начать смену")],
            [KeyboardButton(text="🧹 Мои уборки")]
        ],
        resize_keyboard=True
    )


# -------------------------
# /start
# -------------------------
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Если роль уже выбрана — сразу меню
    if user_id in USER_ROLES:
        role = USER_ROLES[user_id]

        if role == "admin":
            await message.answer("👋 Ты администратор", reply_markup=admin_menu())
        else:
            await message.answer("👋 Ты горничная", reply_markup=housekeeper_menu())
        return

    # Если роли нет — предлагаем выбрать
    await message.answer(
        "Привет! Кто ты?",
        reply_markup=role_keyboard()
    )
    await state.set_state(RoleState.choosing_role)


# -------------------------
# ВЫБОР РОЛИ
# -------------------------
async def choose_housekeeper(message: Message, state: FSMContext):
    USER_ROLES[message.from_user.id] = "housekeeper"
    await state.clear()

    await message.answer(
        "👩‍🧹 Роль сохранена: горничная",
        reply_markup=housekeeper_menu()
    )


async def choose_admin(message: Message, state: FSMContext):
    USER_ROLES[message.from_user.id] = "admin"
    await state.clear()

    await message.answer(
        "🧑‍💼 Роль сохранена: администратор",
        reply_markup=admin_menu()
    )


# -------------------------
# MAIN
# -------------------------
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, CommandStart())
    dp.message.register(
        choose_housekeeper,
        RoleState.choosing_role,
        lambda m: "горничная" in m.text.lower()
    )
    dp.message.register(
        choose_admin,
        RoleState.choosing_role,
        lambda m: "администратор" in m.text.lower()
    )

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
