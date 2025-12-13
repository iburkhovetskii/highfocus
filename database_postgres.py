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
            
            # Новая таблица для всех ответов (основные + High Focus вопросы)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS complete_quiz_answers (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    focus_type TEXT,
                    
                    -- Основные вопросы о типе мозга (q1-q5)
                    q1_type TEXT,
                    q1_text TEXT,
                    q2_type TEXT,
                    q2_text TEXT,
                    q3_type TEXT,
                    q3_text TEXT,
                    q4_type TEXT,
                    q4_text TEXT,
                    q5_type TEXT,
                    q5_text TEXT,
                    
                    -- Дополнительные вопросы о High Focus
                    -- Вопрос 1
                    highfocus_q1_correct_text TEXT,
                    highfocus_q1_wrong_answers TEXT,  -- JSON массив с неправильными ответами
                    highfocus_q1_attempts INTEGER,
                    -- Вопрос 2
                    highfocus_q2_correct_text TEXT,
                    highfocus_q2_wrong_answers TEXT,  -- JSON массив с неправильными ответами
                    highfocus_q2_attempts INTEGER,
                    -- Вопрос 3
                    highfocus_q3_correct_text TEXT,
                    highfocus_q3_wrong_answers TEXT,  -- JSON массив с неправильными ответами
                    highfocus_q3_attempts INTEGER,
                    
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Таблица промокодов
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS promo_codes (
                    id SERIAL PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    user_id BIGINT,
                    used_at TIMESTAMP,
                    is_used BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Таблица для отслеживания выданных промокодов пользователям
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_promo_codes (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    promo_code TEXT NOT NULL,
                    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id)
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
    
    async def save_complete_quiz(self, user_id: int, focus_type: str, answers: dict, 
                                  highfocus_wrong: dict):
        """
        Сохранение полного прохождения квиза (все ответы в одной записи)
        
        Args:
            user_id: ID пользователя
            focus_type: Определенный тип мозга
            answers: Словарь с ответами на все вопросы
            highfocus_wrong: Словарь с неправильными ответами на вопросы High Focus
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO complete_quiz_answers (
                    user_id, focus_type,
                    q1_type, q1_text, q2_type, q2_text, q3_type, q3_text,
                    q4_type, q4_text, q5_type, q5_text,
                    highfocus_q1_correct_text, highfocus_q1_wrong_answers, highfocus_q1_attempts,
                    highfocus_q2_correct_text, highfocus_q2_wrong_answers, highfocus_q2_attempts,
                    highfocus_q3_correct_text, highfocus_q3_wrong_answers, highfocus_q3_attempts
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                        $13, $14, $15, $16, $17, $18, $19, $20, $21)
            """,
                user_id, focus_type,
                answers.get('q1', {}).get('type'), answers.get('q1', {}).get('text'),
                answers.get('q2', {}).get('type'), answers.get('q2', {}).get('text'),
                answers.get('q3', {}).get('type'), answers.get('q3', {}).get('text'),
                answers.get('q4', {}).get('type'), answers.get('q4', {}).get('text'),
                answers.get('q5', {}).get('type'), answers.get('q5', {}).get('text'),
                answers.get('highfocus_q1', {}).get('text'),
                json.dumps(highfocus_wrong.get('q1', []), ensure_ascii=False),
                len(highfocus_wrong.get('q1', [])) + 1,  # +1 за правильный ответ
                answers.get('highfocus_q2', {}).get('text'),
                json.dumps(highfocus_wrong.get('q2', []), ensure_ascii=False),
                len(highfocus_wrong.get('q2', [])) + 1,
                answers.get('highfocus_q3', {}).get('text'),
                json.dumps(highfocus_wrong.get('q3', []), ensure_ascii=False),
                len(highfocus_wrong.get('q3', [])) + 1
            )
    
    async def get_complete_quiz_by_user(self, user_id: int):
        """Получение полных результатов квиза пользователя"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT * FROM complete_quiz_answers
                WHERE user_id = $1
                ORDER BY completed_at DESC
            """, user_id)

    # ===== Методы для работы с промокодами =====
    
    async def load_promo_codes_from_list(self, codes: list):
        """Загрузка промокодов из списка в БД (пропускает уже существующие)"""
        async with self.pool.acquire() as conn:
            for code in codes:
                code = code.strip()
                if code:
                    await conn.execute("""
                        INSERT INTO promo_codes (code, is_used)
                        VALUES ($1, FALSE)
                        ON CONFLICT (code) DO NOTHING
                    """, code)
    
    async def get_user_promo_code(self, user_id: int) -> str | None:
        """Получить промокод, который уже был выдан пользователю"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT promo_code FROM user_promo_codes
                WHERE user_id = $1
            """, user_id)
            return row['promo_code'] if row else None
    
    async def assign_promo_code_to_user(self, user_id: int) -> str | None:
        """
        Выдать уникальный промокод пользователю.
        Если пользователь уже получал промокод — вернуть его.
        Если свободных промокодов нет — вернуть None.
        """
        async with self.pool.acquire() as conn:
            # Проверяем, есть ли уже промокод у пользователя
            existing = await conn.fetchrow("""
                SELECT promo_code FROM user_promo_codes
                WHERE user_id = $1
            """, user_id)
            
            if existing:
                return existing['promo_code']
            
            # Берём первый свободный промокод и блокируем его
            async with conn.transaction():
                row = await conn.fetchrow("""
                    SELECT id, code FROM promo_codes
                    WHERE is_used = FALSE
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """)
                
                if not row:
                    return None  # Нет свободных промокодов
                
                promo_code = row['code']
                promo_id = row['id']
                
                # Помечаем промокод как использованный
                await conn.execute("""
                    UPDATE promo_codes
                    SET is_used = TRUE, user_id = $1, used_at = CURRENT_TIMESTAMP
                    WHERE id = $2
                """, user_id, promo_id)
                
                # Сохраняем связь пользователь-промокод
                await conn.execute("""
                    INSERT INTO user_promo_codes (user_id, promo_code)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id) DO NOTHING
                """, user_id, promo_code)
                
                return promo_code
    
    async def get_promo_stats(self):
        """Статистика по промокодам"""
        async with self.pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM promo_codes")
            used = await conn.fetchval("SELECT COUNT(*) FROM promo_codes WHERE is_used = TRUE")
            return {"total": total, "used": used, "available": total - used}

    async def close(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
