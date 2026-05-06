from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.states.reply import ReplyState

router = Router()


@router.callback_query(F.data.startswith("reply_"))
async def reply(call: CallbackQuery, state: FSMContext):
    target = int(call.data.split("_")[1])

    await state.update_data(target=target)
    await state.set_state(ReplyState.waiting_text)

    await call.message.answer("✍️ Напиши ответ")


@router.message(ReplyState.waiting_text)
async def process_reply(message: Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    target = data["target"]

    await bot.send_message(
        target,
        f"💬 Анонимный ответ:\n\n{message.text}"
    )

    await state.clear()

    await message.answer("✅ Отправлено")


@router.callback_query()
async def unknown_callback(call: CallbackQuery):
    await call.answer("❗ Кнопка устарела", show_alert=True)
