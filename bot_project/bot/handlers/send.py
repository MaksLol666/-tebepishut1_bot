from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.states.reply import SendMessage

router = Router()


@router.message(SendMessage.waiting_for_message)
async def process_message(message: Message, state: FSMContext):

    data = await state.get_data()

    target_id = int(data["target_id"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Ответить",
                    callback_data=f"reply_{message.from_user.id}"
                )
            ]
        ]
    )

    await message.bot.send_message(
        target_id,
        f"💌 Новое анонимное сообщение:\n\n{message.text}",
        reply_markup=keyboard
    )

    await message.answer("✅ Сообщение отправлено")

    await state.clear()
