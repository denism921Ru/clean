import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------
# ХРАНИЛИЩА (временно в памяти)
# ------------------------

user_roles = {}            # user_id -> "admin" | "housekeeper"
apartments = []            # список квартир (строки)
admin_states = {}          # user_id -> состояние ("adding_apartment")

# ------------------------
# КЛАВИАТУРЫ
# ------------------------

def role_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍💼 Я администратор")],
            [KeyboardButton(text="🧹 Я горничная")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Квартиры")],
            [KeyboardButton(text="➕ Назначить уборку")]
        ],
        resize_keyboard=True
    )


def housekeeper_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="▶️ Начать смену")],
            [KeyboardButton(text="📋 Мои уборки")]
        ],
        resize_keyboard=True
    )


def apartments_menu():
    keyboard = [[KeyboardButton(text=addr)] for addr in apartments]
    keyboard.append([KeyboardButton(text="➕ Добавить квартиру")])
    keyboard.append([KeyboardButton(text="⬅️ Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# ------------------------
# /start
# ------------------------

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id

    if user_id not in user_roles:
        await message.answer(
            "Привет! Выбери свою роль 👇",
            reply_markup=role_keyboard()
        )
    else:
        role = user_roles[user_id]
        if role == "admin":
            await message.answer(
                "Ты вошёл как администратор 👨‍💼",
                reply_markup=admin_menu()
            )
        else:
            await message.answer(
                "Ты вошла как горничная 🧹",
                reply_markup=housekeeper_menu()
            )

# ------------------------
# ВЫБОР РОЛИ
# ------------------------

@dp.message(F.text == "👨‍💼 Я администратор")
async def set_admin(message: Message):
    user_roles[message.from_user.id] = "admin"
    await message.answer(
        "Роль сохранена: администратор 👨‍💼",
        reply_markup=admin_menu()
    )


@dp.message(F.text == "🧹 Я горничная")
async def set_housekeeper(message: Message):
    user_roles[message.from_user.id] = "housekeeper"
    await message.answer(
        "Роль сохранена: горничная 🧹",
        reply_markup=housekeeper_menu()
    )

# ------------------------
# АДМИНИСТРАТОР — КВАРТИРЫ
# ------------------------

@dp.message(F.text == "📍 Квартиры")
async def show_apartments(message: Message):
    if not apartments:
        await message.answer(
            "Список квартир пуст.",
            reply_markup=apartments_menu()
        )
    else:
        await message.answer(
            "Список квартир:",
            reply_markup=apartments_menu()
        )


@dp.message(F.text == "➕ Добавить квартиру")
async def add_apartment_start(message: Message):
    admin_states[message.from_user.id] = "adding_apartment"
    await message.answer(
        "Введите адрес квартиры текстом:"
    )


@dp.message(F.text == "⬅️ Назад")
async def back_to_admin_menu(message: Message):
    await message.answer(
        "Меню администратора",
        reply_markup=admin_menu()
    )


@dp.message()
async def handle_text(message: Message):
    user_id = message.from_user.id

    # Добавление квартиры
    if admin_states.get(user_id) == "adding_apartment":
        apartments.append(message.text)
        admin_states.pop(user_id)

        await message.answer(
            f"Квартира добавлена:\n📍 {message.text}",
            reply_markup=apartments_menu()
        )
        return

    # Горничная — начало смены (пока заглушка)
    if message.text == "▶️ Начать смену":
        await message.answer(
            "Смена начата.\nНазначенные уборки появятся здесь.",
            reply_markup=housekeeper_menu()
        )
        return


# ------------------------
# ЗАПУСК
# ------------------------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
