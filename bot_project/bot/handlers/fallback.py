from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def fallback(message: Message):
    await message.answer(
        "🤖 Я не понял это действие.\n\n"
        "Используй кнопки меню 👇"
    )
