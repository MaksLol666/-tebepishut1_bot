from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📬 Мои сообщения")
async def my_messages(message: Message):
    await message.answer("📬 У тебя пока нет сообщений")


@router.message(F.text == "👥 Пригласить")
async def invite(message: Message):
    await message.answer("🔗 Поделись своей ссылкой из меню")


@router.message(F.text == "📩 Моя ссылка")
async def fake_link(message: Message):
    await message.answer("ℹ️ Ссылка генерируется в разделе 'Моя ссылка'")
