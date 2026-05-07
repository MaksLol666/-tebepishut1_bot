import asyncio
import logging
import sys
import os

# 🔥 FIX ДЛЯ BOTHOST
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from aiogram import Dispatcher

from bot.loader import bot
from bot.db.database import init_db

# handlers
from bot.handlers.start import router as start_router
from bot.handlers.link import router as link_router
from bot.handlers.send import router as send_router
from bot.handlers.reply import router as reply_router
from bot.handlers.admin import router as admin_router
from bot.handlers.menu import router as menu_router
from bot.handlers.inbox import router as inbox_router
from bot.handlers.fallback import router as fallback_router

# dispatcher
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)

    # init database
    await init_db()

    # register routers
    dp.include_router(start_router)
    dp.include_router(link_router)
    dp.include_router(send_router)
    dp.include_router(reply_router)
    dp.include_router(admin_router)
    dp.include_router(menu_router)
    dp.include_router(inbox_router)
    dp.include_router(fallback_router)

    print("✅ BOT STARTED SUCCESSFULLY")

    # start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
