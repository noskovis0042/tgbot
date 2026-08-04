from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

# ---------------- BOT ----------------

TOKEN = "token"

bot = Bot(TOKEN)

dp = Dispatcher()


# ----------------------------------------------------------
# /start
# ----------------------------------------------------------

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("todo")
