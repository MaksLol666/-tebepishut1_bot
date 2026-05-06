from aiogram import Router, F
from aiogram.types import Message
import aiosqlite

router = Router()


@router.message(F.text == "📬 Мои сообщения")
async def inbox(message: Message):

    async with aiosqlite.connect("db.sqlite3") as db:
        cursor = await db.execute(
            "SELECT text FROM messages WHERE to_user=? ORDER BY id DESC LIMIT 5",
            (message.from_user.id,)
        )

        rows = await cursor.fetchall()

    if not rows:
        await message.answer("📭 У тебя пока нет сообщений")
        return

    text = "📬 Последние сообщения:\n\n"

    for i, row in enumerate(rows, 1):
        text += f"{i}. 💌 {row[0]}\n\n"

    await message.answer(text)
