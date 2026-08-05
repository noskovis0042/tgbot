import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

# ---------------- BOT ----------------

TOKEN = "token"

bot = Bot(TOKEN)
dp = Dispatcher()


# ----------------------------------------------------------
# БД
# ----------------------------------------------------------

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
    await message.answer("todo")


# ----------------------------------------------------------
# Запуск бота
# ----------------------------------------------------------

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
