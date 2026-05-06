from aiogram import Router, F
from aiogram.types import Message

from bot.db.database import update_user
from bot.config import BOT_USERNAME

router = Router()


@router.message(F.text == "📩 Моя ссылка")
async def link(message: Message):
    await update_user(message.from_user.id)

    url = f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"

    await message.answer(f"🔗 Твоя ссылка:\n{url}")
