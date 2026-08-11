import aiosqlite

DB_NAME = "broker.db"

async def setup_db():
    #init user table if it doesnt exist
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 100,
                last_daily REAL DEFAULT 0,
                last_rob REAL DEFAULT 0
            )
        ''')
        await db.commit()

async def get_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT balance, last_daily, last_rob FROM users WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
        if user is None:
            #insert new user
            await db.execute("INSERT INTO users (user_id, username, balance) VALUES (?, ?, 100)", (user_id, username))
            await db.commit()
            return (100, 0, 0)
        return user

async def update_balance(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()

async def update_cooldown(user_id, column, timestamp):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (timestamp, user_id))
        await db.commit()

async def get_top_users(limit=5):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT username, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,)) as cursor:
            return await cursor.fetchall()