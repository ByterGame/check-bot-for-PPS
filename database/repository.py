import aiosqlite
from config import DB_NAME

async def upsert_user(username: str, surname: str, link: str, bot_name: str, tests_passed: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT tests_passed FROM users WHERE username = ?", 
            (username,)
        ) as cursor:
            row = await cursor.fetchone()
        
        if row is None:
            await db.execute(
                '''INSERT INTO users (username, surname, git_link, bot_name, tests_passed)
                   VALUES (?, ?, ?, ?, ?)''',
                (username, surname, link, bot_name, tests_passed)
            )
        else:
            current_tests = row[0]
            if tests_passed > current_tests:
                await db.execute(
                    '''UPDATE users 
                       SET surname = ?, git_link = ?, bot_name = ?, tests_passed = ?
                       WHERE username = ?''',
                    (surname, link, bot_name, tests_passed, username)
                )
            else:
                return False
        
        await db.commit()
        return True

async def export_all_to_txt(file_path: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT username, surname, git_link, bot_name, tests_passed FROM users") as cursor:
            rows = await cursor.fetchall()
    
    with open(file_path, "w", encoding="utf-8") as f:
        for row in rows:
            username, surname, link, bot_name, tests_count = row
            line = f"{username} - {surname or 'N/A'} - {link or 'N/A'} - {bot_name or 'N/A'} - {tests_count}\n"
            f.write(line)
    
    return file_path