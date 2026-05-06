from aiogram import Router, F
from aiogram.types import Message
from bot.config import BOT_USERNAME

router = Router()


@router.message(F.text == "📩 Моя ссылка")
async def link(message: Message):

    url = f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"

    await message.answer(f"🔗 Твоя ссылка:\n{url}")
