from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📬 Мои сообщения")
async def my_messages(message: Message):
    await message.answer("📬 Тут будут твои сообщения")
