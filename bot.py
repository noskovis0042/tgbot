import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# ---------------- BOT ----------------

TOKEN = "token"

bot = Bot(TOKEN)
dp = Dispatcher()


# ----------------------------------------------------------
# БД
# ----------------------------------------------------------

# Команда для создания бд в pgadmin
# CREATE TABLE users (
#     id SERIAL PRIMARY KEY,
#     telegram_id BIGINT UNIQUE NOT NULL,
#     username TEXT,
#     registration_date TIMESTAMP DEFAULT NOW()
# );


async def connect_db():
    global db

    db = await asyncpg.connect(
        user="postgres",
        password="123",
        database="telegram_bot",
        host="localhost",
        port=5432
    )

    print("База данных подключена!")


# ----------------------------------------------------------
# /start
# ----------------------------------------------------------

@dp.message(CommandStart())
async def start(message: Message):
    user = await db.fetchrow(
        """
        SELECT *
        FROM users
        WHERE telegram_id = $1
        """,
        message.from_user.id
    )

    if user is None:
        await db.execute(
            """
            INSERT INTO users
            (telegram_id, username)
            VALUES ($1, $2)
            """,
            message.from_user.id,
            message.from_user.username
        )

        await message.answer("Регистрация завершена!")

    else:
        await message.answer("С возвращением!")


# ----------------------------------------------------------
# /profile
# ----------------------------------------------------------

@dp.message(Command("profile"))
async def profile(message: Message):
    user = await db.fetchrow(
        """
        SELECT *
        FROM users
        WHERE telegram_id = $1
        """,
        message.from_user.id
    )

    if user is None:
        await message.answer("Вы не зарегистрированы.")
        return

    text = (
        f"Telegram ID: {user['telegram_id']}\n"
        f"Username: {user['username']}\n"
        f"Дата регистрации: {user['registration_date']}"
    )

    await message.answer(text)


# ----------------------------------------------------------
# Запуск бота
# ----------------------------------------------------------

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
