@echo off
chcp 65001 >nul
echo 🚀 Запуск High Focus Bot...
echo.

REM Проверка наличия виртуального окружения
if not exist "venv\" (
    echo ⚠️  Виртуальное окружение не найдено. Создаём...
    python -m venv venv
    echo ✅ Виртуальное окружение создано
)

REM Активация виртуального окружения
echo 🔧 Активация виртуального окружения...
call venv\Scripts\activate

REM Проверка зависимостей
python -c "import aiogram" 2>nul
if errorlevel 1 (
    echo 📦 Установка зависимостей...
    pip install -r requirements.txt
    echo ✅ Зависимости установлены
)

REM Проверка файла .env
if not exist ".env" (
    echo.
    echo ❌ Файл .env не найден!
    echo 📝 Создайте файл .env и добавьте в него:
    echo    BOT_TOKEN=your_token_here
    echo.
    pause
    exit /b 1
)

REM Запуск бота
echo.
echo ✅ Всё готово! Запуск бота...
echo 📌 Для остановки нажмите Ctrl+C
echo.
python bot.py
pause

