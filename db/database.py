import aiosqlite
import time

DB_PATH = "db.sqlite3"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:

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
            replied INTEGER DEFAULT 0,
            created_at INTEGER
        )
        """)

        await db.commit()


async def update_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.execute(
            "UPDATE users SET last_active=? WHERE user_id=?",
            (int(time.time()), user_id)
        )
        await db.commit()
