"""Скрипт для выгрузки данных из Railway PostgreSQL в CSV"""
import asyncio
import asyncpg
import csv
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


async def export_to_csv():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL не найден в .env")
        print("Получите DATABASE_URL из Railway Dashboard:")
        print("1. Зайдите в PostgreSQL сервис")
        print("2. Variables → DATABASE_URL")
        print("3. Скопируйте и добавьте в .env файл")
        return
    
    try:
        # Подключаемся к БД
        conn = await asyncpg.connect(database_url)
        print("✅ Подключено к Railway PostgreSQL")
        
        # Получаем всех пользователей
        users = await conn.fetch("SELECT * FROM users ORDER BY started_at DESC")
        print(f"📊 Найдено пользователей: {len(users)}")
        
        # Получаем все результаты квизов
        results = await conn.fetch("""
            SELECT qr.*, u.username, u.first_name 
            FROM quiz_results qr
            LEFT JOIN users u ON qr.user_id = u.user_id
            ORDER BY qr.completed_at DESC
        """)
        print(f"📊 Найдено результатов квизов: {len(results)}")
        
        # Экспортируем пользователей
        if users:
            filename_users = f"railway_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_users, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['user_id', 'username', 'first_name', 'started_at'])
                for user in users:
                    writer.writerow([
                        user['user_id'],
                        user['username'] or '',
                        user['first_name'] or '',
                        user['started_at']
                    ])
            print(f"✅ Пользователи экспортированы в {filename_users}")
        
        # Экспортируем результаты квизов
        if results:
            filename_results = f"railway_quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_results, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'user_id', 'username', 'first_name', 
                    'focus_type', 'completed_at', 'answers'
                ])
                for result in results:
                    answers = json.loads(result['answers']) if result['answers'] else {}
                    answers_str = json.dumps(answers, ensure_ascii=False)
                    writer.writerow([
                        result['id'],
                        result['user_id'],
                        result['username'] or '',
                        result['first_name'] or '',
                        result['focus_type'],
                        result['completed_at'],
                        answers_str
                    ])
            print(f"✅ Результаты квизов экспортированы в {filename_results}")
            
            # Детальный экспорт с развёрнутыми ответами
            filename_detailed = f"railway_quiz_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_detailed, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'user_id', 'username', 'first_name', 'focus_type', 'completed_at',
                    'q1_type', 'q1_text', 'q2_type', 'q2_text', 'q3_type', 'q3_text',
                    'q4_type', 'q4_text', 'q5_type', 'q5_text', 'q6_type', 'q6_text',
                    'q7_text', 'q8_text'
                ])
                for result in results:
                    answers = json.loads(result['answers']) if result['answers'] else {}
                    row = [
                        result['id'],
                        result['user_id'],
                        result['username'] or '',
                        result['first_name'] or '',
                        result['focus_type'],
                        result['completed_at']
                    ]
                    # Добавляем ответы на вопросы 1-6
                    for i in range(1, 7):
                        q_key = f'q{i}'
                        if q_key in answers and isinstance(answers[q_key], dict):
                            row.append(answers[q_key].get('type', ''))
                            row.append(answers[q_key].get('text', ''))
                        else:
                            row.append('')
                            row.append('')
                    # Добавляем ответы на вопросы 7-8 (только текст)
                    for i in range(7, 9):
                        q_key = f'q{i}'
                        if q_key in answers and isinstance(answers[q_key], dict):
                            row.append(answers[q_key].get('text', ''))
                        else:
                            row.append('')
                    writer.writerow(row)
            print(f"✅ Детальные результаты экспортированы в {filename_detailed}")
        
        await conn.close()
        print("\n🎉 Экспорт завершён!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(export_to_csv())

