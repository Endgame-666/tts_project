import sqlite3
import aiosqlite
from typing import Optional

class DatabaseMessageManager:
    def __init__(self, db_name: str = "bot.db"):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Создаем таблицу для сообщений"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    file_path TEXT PRIMARY KEY,
                    message_text TEXT NOT NULL,
                    hero_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    async def save_message(self, file_path: str, message_text: str, hero_id: int):
        """Сохраняет сообщение в базу"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT OR REPLACE INTO messages
                (file_path, message_text, hero_id)
                VALUES (?, ?, ?)
            ''', (file_path, message_text, hero_id))
            await db.commit()

    async def get_message_text(self, file_path: str) -> Optional[str]:
        """Получает текст сообщения по пути файла"""
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT message_text, hero_id FROM messages WHERE file_path = ?',
                (file_path,)
            )
            result = await cursor.fetchone()
            if result:
                return {
                    "text": result[0],
                    "character": result[1]
                }
            return None

    async def delete_message(self, file_path: str) -> bool:
        """Удаляет сообщение из базы по пути файла"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(
                    'DELETE FROM messages WHERE file_path = ?',
                    (file_path,)
                )
                if await db.total_changes > 0:
                    await db.commit()
                    return True
                return False
        except Exception as e:
            print(e)
            return False