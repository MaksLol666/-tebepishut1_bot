from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
