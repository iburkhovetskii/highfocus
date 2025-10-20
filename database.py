import aiosqlite
import json
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "highfocus.db"):
        self.db_path = db_path

    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    focus_type TEXT,
                    answers TEXT,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            await db.commit()

    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Добавление пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            """, (user_id, username, first_name))
            await db.commit()

    async def save_quiz_result(self, user_id: int, focus_type: str, answers: dict):
        """Сохранение результатов квиза"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO quiz_results (user_id, focus_type, answers)
                VALUES (?, ?, ?)
            """, (user_id, focus_type, json.dumps(answers, ensure_ascii=False)))
            await db.commit()

    async def get_user_stats(self, user_id: int):
        """Получение статистики пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT focus_type, completed_at 
                FROM quiz_results 
                WHERE user_id = ?
                ORDER BY completed_at DESC
            """, (user_id,)) as cursor:
                return await cursor.fetchall()

    async def get_all_results_stats(self):
        """Получение общей статистики"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT focus_type, COUNT(*) as count
                FROM quiz_results
                GROUP BY focus_type
            """) as cursor:
                return await cursor.fetchall()

