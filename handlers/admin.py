from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_ID

router = Router()


@router.message(F.text.startswith("/broadcast"))
async def broadcast(message: Message, bot):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast", "").strip()

    await message.answer(f"📢 {text} отправка...")
