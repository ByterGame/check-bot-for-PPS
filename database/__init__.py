import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                surname TEXT,
                git_link TEXT,
                bot_name TEXT,
                tests_passed INTEGER DEFAULT 0
            )
        ''')
        await db.commit()
    
