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
        
        # Получаем все ответы High Focus (старая таблица, если существует)
        try:
            highfocus_answers = await conn.fetch("""
                SELECT ha.*, u.username, u.first_name
                FROM highfocus_answers ha
                LEFT JOIN users u ON ha.user_id = u.user_id
                ORDER BY ha.answered_at DESC
            """)
            print(f"📊 Найдено ответов на вопросы High Focus (старая таблица): {len(highfocus_answers)}")
        except:
            highfocus_answers = []
            print(f"⚠️  Старая таблица highfocus_answers не найдена (это нормально)")
        
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
            
            # Детальный экспорт с развёрнутыми ответами (обновлено для 5 вопросов + High Focus)
            filename_detailed = f"railway_quiz_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_detailed, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'user_id', 'username', 'first_name', 'brain_type', 'completed_at',
                    'q1_type', 'q1_text', 'q2_type', 'q2_text', 'q3_type', 'q3_text',
                    'q4_type', 'q4_text', 'q5_type', 'q5_text',
                    'highfocus_q1_text', 'highfocus_q1_correct', 'highfocus_q1_wrong', 'highfocus_q1_attempts',
                    'highfocus_q2_text', 'highfocus_q2_correct', 'highfocus_q2_wrong', 'highfocus_q2_attempts',
                    'highfocus_q3_text', 'highfocus_q3_correct', 'highfocus_q3_wrong', 'highfocus_q3_attempts'
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
                    # Добавляем ответы на вопросы 1-5
                    for i in range(1, 6):
                        q_key = f'q{i}'
                        if q_key in answers and isinstance(answers[q_key], dict):
                            row.append(answers[q_key].get('type', ''))
                            row.append(answers[q_key].get('text', ''))
                        else:
                            row.append('')
                            row.append('')
                    
                    # Добавляем данные о High Focus вопросах
                    highfocus_attempts = answers.get('highfocus_attempts', {})
                    for i in range(1, 4):
                        hf_key = f'highfocus_q{i}'
                        q_key = f'q{i}'
                        
                        # Правильный ответ
                        if hf_key in answers and isinstance(answers[hf_key], dict):
                            row.append(answers[hf_key].get('text', ''))
                            row.append(answers[hf_key].get('is_correct', False))
                        else:
                            row.append('')
                            row.append(False)
                        
                        # Неправильные ответы и попытки
                        if q_key in highfocus_attempts:
                            wrong_ans = highfocus_attempts[q_key].get('wrong_answers', [])
                            row.append(json.dumps(wrong_ans, ensure_ascii=False) if wrong_ans else '')
                            row.append(highfocus_attempts[q_key].get('attempts', 0))
                        else:
                            row.append('')
                            row.append(0)
                    
                    writer.writerow(row)
            print(f"✅ Детальные результаты экспортированы в {filename_detailed}")
        
        # Экспортируем ответы на вопросы High Focus (если старая таблица существует)
        if highfocus_answers:
            filename_highfocus = f"railway_highfocus_answers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename_highfocus, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'user_id', 'username', 'first_name', 'question_number',
                    'answer_text', 'is_correct', 'answered_at'
                ])
                for answer in highfocus_answers:
                    writer.writerow([
                        answer['id'],
                        answer['user_id'],
                        answer['username'] or '',
                        answer['first_name'] or '',
                        answer['question_number'],
                        answer['answer_text'],
                        answer['is_correct'],
                        answer['answered_at']
                    ])
            print(f"✅ Ответы на вопросы High Focus экспортированы в {filename_highfocus}")
        
        await conn.close()
        print("\n🎉 Экспорт завершён!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(export_to_csv())

