import asyncio
import logging

from bot.loader import bot, dp
from bot.db.database import init_db

from bot.handlers import (
    start,
    link,
    reply,
    admin,
    menu,
    fallback
)


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    dp.include_router(start.router)
    dp.include_router(link.router)
    dp.include_router(reply.router)
    dp.include_router(admin.router)

    # 🔥 ДОБАВЛЕНО:
    dp.include_router(menu.router)
    dp.include_router(fallback.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
