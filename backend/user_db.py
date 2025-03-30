import sqlite3
import json
from typing import Optional
import aiosqlite

class DatabaseManager:
    def __init__(self, db_name: str = "bot.db"):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Создаем бд если еще нет"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT,
                    favourite_messages TEXT
                )
            ''')

            conn.commit()

    async def add_user(self, user_id: int, user_name: str) -> bool:
        """Добавляем нового пользователя, если еще не добавили"""
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT user_id FROM users WHERE user_id = ?',
                (user_id,)
            )
            exists = await cursor.fetchone()

            if not exists:
                await db.execute('''
                    INSERT INTO users (
                        user_id, user_name, favourite_messages
                    ) VALUES (?, ?, ?)
                ''', (
                    user_id, user_name,
                    json.dumps([])
                ))
                await db.commit()
                return True
            return False

    async def get_user(self, user_id: int) -> Optional[dict]:
        """Берем данные пользователя через user_id"""
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT * FROM users WHERE user_id = ?',
                (user_id,)
            )
            user = await cursor.fetchone()

            if user:
                column_names = [description[0] for description in cursor.description]
                user_dict = dict(zip(column_names, user))
                user_dict['favourite_messages'] = json.loads(user_dict['favourite_messages'])
                return user_dict
            return None

    async def update_favourite_messages(self, user_id: int, message_file: str):
        """Добавляем сообщение в избранное"""
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT favourite_messages FROM users WHERE user_id = ?',
                (user_id,)
            )
            favourites_json = await cursor.fetchone()

            if favourites_json:
                favourites = json.loads(favourites_json[0])
                if message_file not in favourites:
                    favourites.append(message_file)
                    await db.execute(
                        'UPDATE users SET favourite_messages = ? WHERE user_id = ?',
                        (json.dumps(favourites), user_id)
                    )
                    await db.commit()

    async def remove_from_favourites(self, user_id: int, file_path: str):
        """Удаляет сообщение из избранного"""
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                'SELECT favourite_messages FROM users WHERE user_id = ?',
                (user_id,)
            )
            result = await cursor.fetchone()

            if not result or not result[0]:
                return

            favourites = json.loads(result[0])
            if file_path in favourites:
                favourites.remove(file_path)

                await db.execute(
                    'UPDATE users SET favourite_messages = ? WHERE user_id = ?',
                    (json.dumps(favourites), user_id)
                )
                await db.commit()
