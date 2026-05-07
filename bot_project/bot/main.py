import asyncio
import logging
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from bot.loader import bot, dp
from bot.db.database import init_db

from bot.handlers import start, link, send, inbox


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    dp.include_router(start.router)
    dp.include_router(link.router)
    dp.include_router(send.router)
    dp.include_router(inbox.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
