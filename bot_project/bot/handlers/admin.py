from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import aiosqlite

router = Router()

ADMIN_ID = 1691654877


@router.message(Command("admin"))
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🛠 Админ панель\n\n"
        "/broadcast текст\n"
        "/ban user_id"
    )


@router.message(Command("broadcast"))
async def broadcast(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast", "").strip()

    if not text:
        await message.answer("❌ Введи текст")
        return

    async with aiosqlite.connect("db.sqlite3") as db:
        cursor = await db.execute(
            "SELECT user_id FROM users"
        )

        users = await cursor.fetchall()

    sent = 0

    for user in users:
        try:
            await message.bot.send_message(
                user[0],
                f"📢 {text}"
            )
            sent += 1
        except:
            pass

    await message.answer(f"✅ Рассылка отправлена: {sent}")


@router.message(Command("ban"))
async def ban_user(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("❌ /ban user_id")
        return

    user_id = args[1]

    async with aiosqlite.connect("db.sqlite3") as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            user_id INTEGER PRIMARY KEY
        )
        """)

        await db.execute(
            "INSERT OR IGNORE INTO bans (user_id) VALUES (?)",
            (user_id,)
        )

        await db.commit()

    await message.answer(f"🚫 Пользователь {user_id} забанен")
