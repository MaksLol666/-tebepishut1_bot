from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.db.database import update_user

router = Router()


@router.message(F.text)
async def send_anonymous(message: Message, state: FSMContext):

    data = await state.get_data()
    target = data.get("target")

    if not target:
        return

    await update_user(message.from_user.id)

    await message.bot.send_message(
        target,
        f"💌 Анонимное сообщение:\n\n{message.text}"
    )

    await message.answer("✅ Отправлено анонимно")

    await state.clear()
