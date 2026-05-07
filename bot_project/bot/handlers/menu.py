from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📬 Мои сообщения")
async def inbox(message: Message):
    await message.answer("📬 Inbox пока пуст")


@router.message(F.text == "👥 Пригласить")
async def invite(message: Message):
    await message.answer("🔗 Поделись своей ссылкой")
