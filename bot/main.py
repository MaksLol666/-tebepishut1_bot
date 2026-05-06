import asyncio
import logging

from loader import bot, dp
from db.database import init_db

from handlers import start, link, messages, reply, admin


async def main():

    logging.basicConfig(level=logging.INFO)

    await init_db()

    dp.include_router(start.router)
    dp.include_router(link.router)
    dp.include_router(messages.router)
    dp.include_router(reply.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
