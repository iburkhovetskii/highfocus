#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт миграции БД - создание таблицы complete_quiz_answers
Запустить один раз для обновления структуры БД
"""

import asyncio
import asyncpg
import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, '/Users/iliaburkhovetskii/highfocus')

from dotenv import load_dotenv

load_dotenv()

async def migrate():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL не найден в .env")
        print("Добавьте DATABASE_URL из Railway в файл .env")
        return
    
    try:
        print("🔄 Подключение к БД...")
        conn = await asyncpg.connect(database_url)
        print("✅ Подключено к PostgreSQL")
        
        print("\n🔧 Создание таблицы complete_quiz_answers...")
        
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
                highfocus_q1_wrong_answers TEXT,
                highfocus_q1_attempts INTEGER,
                -- Вопрос 2
                highfocus_q2_correct_text TEXT,
                highfocus_q2_wrong_answers TEXT,
                highfocus_q2_attempts INTEGER,
                -- Вопрос 3
                highfocus_q3_correct_text TEXT,
                highfocus_q3_wrong_answers TEXT,
                highfocus_q3_attempts INTEGER,
                
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        print("✅ Таблица complete_quiz_answers создана!")
        
        # Проверяем структуру
        columns = await conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'complete_quiz_answers'
            ORDER BY ordinal_position
        """)
        
        print(f"\n📋 Структура таблицы ({len(columns)} колонок):")
        for col in columns:
            print(f"  ✓ {col['column_name']}: {col['data_type']}")
        
        await conn.close()
        print("\n✅ Миграция завершена успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка миграции: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("  МИГРАЦИЯ БД: создание таблицы complete_quiz_answers")
    print("="*60)
    asyncio.run(migrate())


