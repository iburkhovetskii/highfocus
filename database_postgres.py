import asyncpg
import json
import os
from datetime import datetime


class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.pool = None

    async def init_db(self):
        """Инициализация базы данных"""
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Создаём пул соединений
        self.pool = await asyncpg.create_pool(self.database_url)
        
        async with self.pool.acquire() as conn:
            # Создаём таблицы
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    focus_type TEXT,
                    answers TEXT,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Добавление пользователя"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (user_id, username, first_name)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id) DO NOTHING
            """, user_id, username, first_name)

    async def save_quiz_result(self, user_id: int, focus_type: str, answers: dict):
        """Сохранение результатов квиза"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO quiz_results (user_id, focus_type, answers)
                VALUES ($1, $2, $3)
            """, user_id, focus_type, json.dumps(answers, ensure_ascii=False))

    async def get_user_stats(self, user_id: int):
        """Получение статистики пользователя"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT focus_type, completed_at 
                FROM quiz_results 
                WHERE user_id = $1
                ORDER BY completed_at DESC
            """, user_id)

    async def get_all_results_stats(self):
        """Получение общей статистики"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT focus_type, COUNT(*) as count
                FROM quiz_results
                GROUP BY focus_type
            """)

    async def close(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
