from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from db.database import update_user
from keyboards.menu import menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await update_user(message.from_user.id)

    await message.answer(
        "🤫 Тебе пишут\n\nПолучай анонимные сообщения 👀",
        reply_markup=menu
    )
