import asyncio
import logging
import random
import time
import aiosqlite

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ---------------- CONFIG ----------------
TOKEN = "8756367883:AAEJZdghN5Lz0B8R7O1P1NHC5jHya6i4pTA"
BOT_USERNAME = "@tebepishut1_bot"
ADMIN_ID = 1691654877

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- MEMORY ----------------
reply_state = {}
user_last_action = {}

# ---------------- TEXTS ----------------
hints = [
    "👀 Похоже, это кто-то из твоего круга",
    "🤫 Вы точно знакомы",
    "😏 Этот человек часто думает о тебе",
    "🔥 Сообщение эмоциональное",
    "💭 Скорее всего вы недавно общались"
]

fake_events = [
    "👀 Кто-то открыл твою ссылку...",
    "🤫 Кто-то думает тебе написать...",
    "💭 Кто-то печатает сообщение...",
    "👤 Новый человек зашёл...",
    "💌 Тебе скоро напишут..."
]

bad_words = [
    "лох", "идиот", "тупой", "дебил", "сука", "блядь",
    "пидор", "гандон", "шлюха", "урод", "даун",
    "нахуй", "ебать", "пошёл нахуй", "сдохни"
]

# ---------------- DB INIT ----------------
async def init_db():
    async with aiosqlite.connect("db.sqlite3") as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrals INTEGER DEFAULT 0,
            last_active INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_user INTEGER,
            from_user INTEGER,
            text TEXT,
            category TEXT,
            replied INTEGER DEFAULT 0,
            created_at INTEGER
        )
        """)

        await db.commit()

# ---------------- KEYBOARD ----------------
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Моя ссылка")],
        [KeyboardButton(text="📬 Мои сообщения")],
        [KeyboardButton(text="👥 Пригласить")]
    ],
    resize_keyboard=True
)

# ---------------- ACTIVITY ----------------
async def update_activity(user_id):
    async with aiosqlite.connect("db.sqlite3") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        await db.execute(
            "UPDATE users SET last_active = ? WHERE user_id = ?",
            (int(time.time()), user_id)
        )
        await db.commit()

# ---------------- START ----------------
@dp.message(CommandStart())
async def start(message: types.Message):
    await update_activity(message.from_user.id)

    await message.answer(
        "🤫 Тебе пишут\n\nПолучай анонимные сообщения 👀",
        reply_markup=menu
    )

# ---------------- LINK ----------------
@dp.message(F.text == "📩 Моя ссылка")
async def link(message: types.Message):
    await update_activity(message.from_user.id)

    url = f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"

    await message.answer(f"🔗 Твоя ссылка:\n{url}")

# ---------------- BAD WORD FILTER ----------------
def clean(text):
    t = text.lower()
    return any(w in t for w in bad_words)

# ---------------- SEND ANON ----------------
async def send_anonymous(message: types.Message, target_id: int, category: str):

    await update_activity(message.from_user.id)

    text = message.text

    if clean(text):
        await message.answer("🚫 Нельзя отправлять такое")
        return

    # spam protection
    now = time.time()
    if message.from_user.id in user_last_action:
        if now - user_last_action[message.from_user.id] < 5:
            await message.answer("⏳ Подожди немного")
            return

    user_last_action[message.from_user.id] = now

    hint = random.choice(hints)

    async with aiosqlite.connect("db.sqlite3") as db:
        await db.execute("""
            INSERT INTO messages (to_user, from_user, text, category, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (target_id, message.from_user.id, text, category, int(time.time())))
        await db.commit()

    # fake typing
    await bot.send_message(target_id, "💭 Кто-то печатает сообщение...")
    await asyncio.sleep(random.uniform(2, 4))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💬 Ответить анонимно",
            callback_data=f"reply_{target_id}"
        )]
    ])

    await bot.send_message(
        target_id,
        f"{category}\n\n💌 Новое сообщение:\n\n{text}\n\n{hint}",
        reply_markup=keyboard
    )

    await message.answer("✅ Отправлено")

# ---------------- REPLY ----------------
@dp.callback_query(F.data.startswith("reply_"))
async def reply(call: types.CallbackQuery):
    target = int(call.data.split("_")[1])

    reply_state[call.from_user.id] = target

    await call.message.answer("✍️ Напиши ответ (1 раз)")

# ---------------- HANDLE REPLY ----------------
@dp.message()
async def handle_message(message: types.Message):

    if message.from_user.id in reply_state:

        target = reply_state[message.from_user.id]

        text = message.text

        async with aiosqlite.connect("db.sqlite3") as db:

            cursor = await db.execute("""
                SELECT replied FROM messages
                WHERE to_user = ? AND from_user = ?
                ORDER BY id DESC LIMIT 1
            """, (target, message.from_user.id))

            row = await cursor.fetchone()

            if row and row[0] == 1:
                await message.answer("❌ Уже отвечал")
                reply_state.pop(message.from_user.id, None)
                return

            await bot.send_message(
                target,
                f"💬 Анонимный ответ:\n\n{text}"
            )

            await db.execute("""
                UPDATE messages
                SET replied = 1
                WHERE to_user = ? AND from_user = ?
            """, (target, message.from_user.id))

            await db.commit()

        reply_state.pop(message.from_user.id, None)

        await message.answer("✅ Ответ отправлен")
        return

# ---------------- AUTO PUSH ----------------
async def auto_push():
    while True:
        await asyncio.sleep(1800)

        now = int(time.time())

        async with aiosqlite.connect("db.sqlite3") as db:
            cursor = await db.execute("SELECT user_id, last_active FROM users")
            users = await cursor.fetchall()

        for uid, last in users:

            if now - last < 21600:
                continue

            if random.random() > 0.3:
                continue

            try:
                await bot.send_message(uid, random.choice(fake_events))
                await asyncio.sleep(0.1)
            except:
                pass

# ---------------- ADMIN ----------------
@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast", "").strip()

    async with aiosqlite.connect("db.sqlite3") as db:
        cursor = await db.execute("SELECT user_id FROM users")
        users = await cursor.fetchall()

    sent = 0

    for u in users:
        try:
            await bot.send_message(u[0], f"📢 {text}")
            sent += 1
            await asyncio.sleep(0.03)
        except:
            pass

    await message.answer(f"✅ Sent: {sent}")

# ---------------- MAIN ----------------
async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    asyncio.create_task(auto_push())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
