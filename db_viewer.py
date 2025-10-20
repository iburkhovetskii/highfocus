"""
Утилита для просмотра данных из базы данных High Focus Bot
"""
import asyncio
import aiosqlite
from datetime import datetime


async def show_stats():
    """Показывает статистику по базе данных"""
    db_path = "highfocus.db"
    
    print("\n" + "="*60)
    print("📊 СТАТИСТИКА HIGH FOCUS BOT")
    print("="*60 + "\n")
    
    try:
        async with aiosqlite.connect(db_path) as db:
            # Общее количество пользователей
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                count = await cursor.fetchone()
                print(f"👥 Всего пользователей: {count[0]}")
            
            # Общее количество пройденных квизов
            async with db.execute("SELECT COUNT(*) FROM quiz_results") as cursor:
                count = await cursor.fetchone()
                print(f"✅ Пройдено квизов: {count[0]}")
            
            print("\n" + "-"*60)
            print("🎯 РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ФОКУСА")
            print("-"*60 + "\n")
            
            # Распределение по типам фокуса
            async with db.execute("""
                SELECT focus_type, COUNT(*) as count 
                FROM quiz_results 
                GROUP BY focus_type
                ORDER BY count DESC
            """) as cursor:
                results = await cursor.fetchall()
                
                if results:
                    focus_names = {
                        "creative": "💡 Креативный",
                        "analytical": "🧠 Аналитический",
                        "energetic": "⚡️ Энергетический"
                    }
                    
                    total = sum(r[1] for r in results)
                    for focus_type, count in results:
                        percentage = (count / total * 100) if total > 0 else 0
                        name = focus_names.get(focus_type, focus_type)
                        print(f"{name:25} | {count:3} | {percentage:5.1f}%")
                else:
                    print("Нет данных")
            
            print("\n" + "-"*60)
            print("📋 ДЕТАЛЬНЫЕ ОТВЕТЫ (Последние 5)")
            print("-"*60 + "\n")
            
            # Детальные ответы последних пользователей
            async with db.execute("""
                SELECT u.first_name, u.username, r.answers, r.completed_at
                FROM quiz_results r
                JOIN users u ON r.user_id = u.user_id
                ORDER BY r.completed_at DESC
                LIMIT 5
            """) as cursor:
                results = await cursor.fetchall()
                
                if results:
                    import json
                    for idx, (first_name, username, answers_json, completed_at) in enumerate(results, 1):
                        user_display = first_name or username or "Аноним"
                        print(f"\n{idx}. {user_display} ({completed_at}):")
                        try:
                            answers = json.loads(answers_json)
                            for q_num in range(1, 9):
                                answer = answers.get(f"q{q_num}")
                                if answer:
                                    if isinstance(answer, dict):
                                        text = answer.get("text", answer.get("type", "нет ответа"))
                                    else:
                                        text = answer
                                    print(f"   Q{q_num}: {text}")
                        except:
                            print(f"   (ошибка чтения ответов)")
                        print()
                else:
                    print("Нет данных\n")
            
            print("\n" + "-"*60)
            print("📈 ПОСЛЕДНИЕ 10 РЕЗУЛЬТАТОВ")
            print("-"*60 + "\n")
            
            # Последние результаты
            async with db.execute("""
                SELECT u.first_name, u.username, r.focus_type, r.completed_at
                FROM quiz_results r
                JOIN users u ON r.user_id = u.user_id
                ORDER BY r.completed_at DESC
                LIMIT 10
            """) as cursor:
                results = await cursor.fetchall()
                
                if results:
                    focus_emoji = {
                        "creative": "💡",
                        "analytical": "🧠",
                        "energetic": "⚡️"
                    }
                    
                    for first_name, username, focus_type, completed_at in results:
                        emoji = focus_emoji.get(focus_type, "❓")
                        user_display = first_name or username or "Аноним"
                        print(f"{emoji} {user_display:20} | {focus_type:12} | {completed_at}")
                else:
                    print("Нет данных")
            
            print("\n" + "-"*60)
            print("🍹 ПРЕДПОЧТЕНИЯ ПО ВКУСАМ (Вопрос 8)")
            print("-"*60 + "\n")
            
            # Статистика по вопросу 8 (предпочтения по вкусам)
            async with db.execute("""
                SELECT answers FROM quiz_results
            """) as cursor:
                all_answers = await cursor.fetchall()
                
                if all_answers:
                    import json
                    q8_counts = {}
                    
                    for (answers_json,) in all_answers:
                        try:
                            answers = json.loads(answers_json)
                            q8_answer = answers.get("q8")
                            if q8_answer:
                                # Поддержка старого формата (строка) и нового (dict)
                                if isinstance(q8_answer, dict):
                                    answer_text = q8_answer.get("text", q8_answer.get("type", "unknown"))
                                    q8_counts[answer_text] = q8_counts.get(answer_text, 0) + 1
                                else:
                                    # Старый формат
                                    taste_names_old = {
                                        "pear": "🍐 Груша-Пармезан",
                                        "caramel": "🍯 Солёная карамель",
                                        "brownie": "🍫 Брауни",
                                        "want": "🤔 Ещё не пробовал, но хочу",
                                        "undecided": "🤷 Пока не решил"
                                    }
                                    answer_text = taste_names_old.get(q8_answer, q8_answer)
                                    q8_counts[answer_text] = q8_counts.get(answer_text, 0) + 1
                        except:
                            pass
                    
                    if q8_counts:
                        total = sum(q8_counts.values())
                        for taste_text, count in sorted(q8_counts.items(), key=lambda x: x[1], reverse=True):
                            percentage = (count / total * 100) if total > 0 else 0
                            print(f"{taste_text:35} | {count:3} | {percentage:5.1f}%")
                    else:
                        print("Нет данных")
                else:
                    print("Нет данных")
            
    except Exception as e:
        print(f"\n❌ Ошибка при чтении базы данных: {e}")
        print("Убедитесь, что файл highfocus.db существует и бот был запущен хотя бы раз.")
    
    print("\n" + "="*60 + "\n")


async def export_to_csv():
    """Экспорт данных в CSV файл"""
    db_path = "highfocus.db"
    
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("""
                SELECT 
                    u.user_id,
                    u.username,
                    u.first_name,
                    r.focus_type,
                    r.answers,
                    r.completed_at
                FROM quiz_results r
                JOIN users u ON r.user_id = u.user_id
                ORDER BY r.completed_at DESC
            """) as cursor:
                results = await cursor.fetchall()
                
                if results:
                    filename = f"highfocus_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("user_id,username,first_name,focus_type,answers,completed_at\n")
                        for row in results:
                            # Экранируем запятые в answers
                            answers = str(row[4]).replace(',', ';')
                            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},\"{answers}\",{row[5]}\n")
                    
                    print(f"\n✅ Данные экспортированы в файл: {filename}")
                else:
                    print("\n⚠️ Нет данных для экспорта")
                    
    except Exception as e:
        print(f"\n❌ Ошибка при экспорте: {e}")


async def main():
    print("\n🤖 High Focus Bot - Утилита работы с БД")
    print("\nВыберите действие:")
    print("1. Показать статистику")
    print("2. Экспортировать данные в CSV")
    print("0. Выход")
    
    choice = input("\nВаш выбор: ").strip()
    
    if choice == "1":
        await show_stats()
    elif choice == "2":
        await export_to_csv()
    elif choice == "0":
        print("\nДо свидания! 👋")
    else:
        print("\n❌ Неверный выбор")


if __name__ == "__main__":
    asyncio.run(main())

