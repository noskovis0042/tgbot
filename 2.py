import asyncio

# ---------------- AIROGRAM ----------------

from aiogram import Bot, Dispatcher
# from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# ---------------- SQLALCHEMY ----------------

# Создает подключение (Engine) к базе данных.
from sqlalchemy.ext.asyncio import create_async_engine

# Создает асинхронные сессии.
from sqlalchemy.ext.asyncio import async_sessionmaker

# Базовый класс для всех моделей.
from sqlalchemy.orm import DeclarativeBase

# Используется для описания столбцов таблицы.
from sqlalchemy.orm import Mapped, mapped_column

# Типы данных PostgreSQL.
from sqlalchemy import BigInteger, String, DateTime

# Позволяет выполнять SELECT-запросы.
from sqlalchemy import select

# ---------------- НАСТРОЙКИ ----------------

TOKEN = "ВАШ_ТОКЕН"

# Строка подключения к PostgreSQL.
# Формат:
# postgresql+asyncpg://ПОЛЬЗОВАТЕЛЬ:ПАРОЛЬ@ХОСТ/БАЗА
DATABASE_URL = (
    "postgresql+asyncpg://postgres:123@localhost/telegram_bot")

# ---------------- ENGINE ----------------

# Engine — это "двигатель" SQLAlchemy.
# Он знает:
# • куда подключаться;
# • какой пароль использовать;
# • какую базу открыть.
# Сам запросы Engine НЕ выполняет.
engine = create_async_engine(
    DATABASE_URL,
    echo=False)

# ---------------- SESSION ----------------

# Session — это рабочее место.
# Через Session выполняются ВСЕ запросы.
# Каждый раз мы будем создавать новую Session.
Session = async_sessionmaker(engine, expire_on_commit=False)


# ---------------- BASE ----------------

# Все таблицы должны наследоваться от Base.
# Это обязательное требование SQLAlchemy.

class Base(DeclarativeBase):
    pass


# ---------------- МОДЕЛЬ USERS ----------------

# Этот класс описывает таблицу users.
# SQLAlchemy смотрит на этот класс
# и понимает, как выглядит таблица.

class User(Base):
    # Имя таблицы в PostgreSQL.
    __tablename__ = "users"

    # id SERIAL PRIMARY KEY
    id: Mapped[int] = mapped_column(primary_key=True)

    # telegram_id BIGINT
    telegram_id: Mapped[int] = mapped_column(BigInteger)

    # username TEXT
    username: Mapped[str] = mapped_column(String)

    # registration_date TIMESTAMP
    registration_date: Mapped[DateTime]


# ---------------- BOT ----------------

bot = Bot(TOKEN)

dp = Dispatcher()


# ----------------------------------------------------------
# /start
# ----------------------------------------------------------

@dp.message(CommandStart())
async def start(message: Message):
    # Открываем новую Session.
    # После выхода из блока
    # она автоматически закроется.

    async with Session() as session:

        # Формируем SELECT-запрос.
        # Пока он НЕ выполняется.

        request = select(User).where(
            User.telegram_id == message.from_user.id)

        # Выполняем запрос.
        result = await session.execute(request)

        # Получаем пользователя.
        # Если запись не найдена,
        # вернется None.

        user = result.scalar_one_or_none()

        # ---------------------------------

        if user is None:
            # Создаем ОБЫЧНЫЙ объект Python.
            # Пока он существует
            # только в памяти.
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username)
            # Говорим SQLAlchemy:
            # "Подготовь объект к сохранению."
            session.add(new_user)
            # Только сейчас запись попадет в PostgreSQL.
            await session.commit()

            await message.answer("Регистрация завершена")

        else:
            await message.answer("С возвращением")


# ----------------------------------------------------------
# /profile
# ----------------------------------------------------------

@dp.message(Command("profile"))
async def profile(message: Message):
    async with Session() as session:
        # SELECT * FROM users
        # WHERE telegram_id = ...
        request = select(User).where(
            User.telegram_id == message.from_user.id)
        result = await session.execute(request)

        user = result.scalar_one_or_none()

        if user is None:
            await message.answer("Вы не зарегистрированы.")
            return

        # Обратите внимание!
        # В asyncpg было:
        # user["username"]
        # Теперь:
        # user.username
        text = (
            f"Telegram ID: {user.telegram_id}\n"
            f"Username: {user.username}\n"
            f"Регистрация: {user.registration_date}")
        await message.answer(text)


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

async def main():
    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
