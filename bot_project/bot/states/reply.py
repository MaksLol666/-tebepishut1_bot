from aiogram.fsm.state import StatesGroup, State


class ReplyState(StatesGroup):
    waiting_for_message = State()
