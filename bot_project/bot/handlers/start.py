from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.menu import menu
from bot.states.reply import ReplyState

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):

    args = message.text.split()

    # пришли по анонимной ссылке
    if len(args) > 1:

        target_id = args[1]

        # нельзя писать самому себе
        if str(message.from_user.id) == target_id:
            await message.answer("❌ Нельзя отправить сообщение самому себе")
            return

        await state.update_data(target_id=target_id)
        await state.set_state(ReplyState.waiting_for_message)

        await message.answer(
            "✍️ Напиши анонимное сообщение"
        )

        return

    # обычный старт
    await message.answer(
        "🤫 Тебе пишут\n\nВыбери действие 👇",
        reply_markup=menu
    )
