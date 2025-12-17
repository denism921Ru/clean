import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Простое хранилище ролей (позже заменим на БД)
user_roles = {}


def role_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧹 Я горничная")],
            [KeyboardButton(text="👨‍💼 Я администратор")]
        ],
        resize_keyboard=True
    )


def housekeeper_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои уборки")],
            [KeyboardButton(text="▶️ Начать смену")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои горничные")],
            [KeyboardButton(text="➕ Назначить уборку")]
        ],
        resize_keyboard=True
    )


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id

    if user_id not in user_roles:
        await message.answer(
            "Привет! Выбери свою роль:",
            reply_markup=role_keyboard()
        )
    else:
        role = user_roles[user_id]
        if role == "housekeeper":
            await message.answer(
                "Ты вошла как горничная 👇",
                reply_markup=housekeeper_menu()
            )
        else:
            await message.answer(
                "Ты вошёл как администратор 👇",
                reply_markup=admin_menu()
            )


@dp.message(F.text == "🧹 Я горничная")
async def set_housekeeper(message: Message):
    user_roles[message.from_user.id] = "housekeeper"
    await message.answer(
        "Роль сохранена: горничная 🧹",
        reply_markup=housekeeper_menu()
    )


@dp.message(F.text == "👨‍💼 Я администратор")
async def set_admin(message: Message):
    user_roles[message.from_user.id] = "admin"
    await message.answer(
        "Роль сохранена: администратор 👨‍💼",
        reply_markup=admin_menu()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
