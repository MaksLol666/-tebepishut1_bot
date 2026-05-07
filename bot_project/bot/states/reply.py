from aiogram.fsm.state import StatesGroup, State


class SendMessage(StatesGroup):
    waiting_for_message = State()
