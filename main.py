import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN

# ------------------------
# ЛОГИ
# ------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------
# BOT / DP
# ------------------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------
# ВРЕМЕННЫЕ ХРАНИЛИЩА
# (ПОКА БЕЗ GOOGLE SHEETS)
# ------------------------
user_roles = {}  # user_id -> "admin" | "housekeeper"

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

# ------------------------
# /start
# ------------------------
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    logger.info(f"/start от пользователя {user_id}")

    if user_id not in user_roles:
        await message.answer(
            "Привет! 👋\nВыбери свою роль:",
            reply_markup=role_keyboard()
        )
    else:
        role = user_roles[user_id]
        if role == "admin":
            await message.answer(
                "Ты администратор 👨‍💼",
                reply_markup=admin_menu()
            )
        else:
            await message.answer(
                "Ты горничная 🧹",
                reply_markup=housekeeper_menu()
            )

# ------------------------
# ВЫБОР РОЛИ
# ------------------------
@dp.message(F.text == "👨‍💼 Я администратор")
async def set_admin(message: Message):
    user_roles[message.from_user.id] = "admin"
    logger.info(f"Пользователь {message.from_user.id} стал администратором")

    await message.answer(
        "Роль сохранена: администратор 👨‍💼",
        reply_markup=admin_menu()
    )


@dp.message(F.text == "🧹 Я горничная")
async def set_housekeeper(message: Message):
    user_roles[message.from_user.id] = "housekeeper"
    logger.info(f"Пользователь {message.from_user.id} стал горничной")

    await message.answer(
        "Роль сохранена: горничная 🧹",
        reply_markup=housekeeper_menu()
    )

# ------------------------
# ЗАГЛУШКИ (чтобы НЕ МОЛЧАЛ)
# ------------------------
@dp.message()
async def fallback(message: Message):
    logger.info(f"Сообщение от {message.from_user.id}: {message.text}")

    await message.answer(
        "Я получил сообщение 👍\n"
        "Если что-то не появилось — нажми /start"
    )

# ------------------------
# ЗАПУСК
# ------------------------
async def main():
    logger.info("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
