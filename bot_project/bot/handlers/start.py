from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db.database import update_user

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_link(message: Message):
    await update_user(message.from_user.id)

    args = message.text.split()

    # если пришли по ссылке
    if len(args) > 1:
        target_id = args[1]

        message.bot_data = {"target": target_id}

        await message.answer(
            "✍️ Напиши сообщение, которое хочешь отправить анонимно"
        )
        return

    await message.answer(
        "🤫 Тебе пишут\n\nОтправь кому-нибудь свою ссылку 👇"
    )
