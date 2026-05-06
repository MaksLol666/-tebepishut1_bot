from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Моя ссылка")],
        [KeyboardButton(text="📬 Мои сообщения")],
        [KeyboardButton(text="👥 Пригласить")]
    ],
    resize_keyboard=True
)
