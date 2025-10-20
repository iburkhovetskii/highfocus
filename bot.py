import asyncio
import logging
import os
import os as _os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database import Database
from states import QuizStates
from keyboards import (
    get_start_keyboard,
    get_back_to_start_keyboard,
    get_question_1_keyboard,
    get_question_2_keyboard,
    get_question_3_keyboard,
    get_question_4_keyboard,
    get_question_5_keyboard,
    get_question_6_keyboard,
    get_question_7_keyboard,
    get_question_8_keyboard,
    get_final_keyboard
)

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем путь к БД (для Railway с Volume)
DB_PATH = os.getenv("DB_PATH", "/data/highfocus.db")
db = Database(db_path=DB_PATH)

# Admins
raw_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = set()
if raw_admins:
    try:
        ADMIN_IDS = {int(x) for x in raw_admins.replace(" ", "").split(",") if x}
    except Exception:
        ADMIN_IDS = set()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS and len(ADMIN_IDS) > 0

# Тексты
START_TEXT = """⚡️ Привет! Это High Focus — напиток для тех, кто держит ум в тонусе.

Мы созданы, чтобы помогать сохранять концентрацию, энергию и баланс в мире, где информации больше, чем времени.

Хочешь узнать, какой у тебя тип фокуса — и какой вкус High Focus включает тебя на максимум? ⚡️"""

ABOUT_TEXT = """High Focus — это инновационный молочный напиток от ЭкоНивы, созданный для тех, кто работает головой.

В составе:
☕️ гуарана — мягкая энергия,
🍃 L-теанин — концентрация и баланс,
💊 витамины группы B — поддержка мозга и настроения.

Без сахарозы. Без лактозы. Только чистый фокус и энергия."""

QUESTIONS = {
    1: "1️⃣ Когда тебе нужно сосредоточиться, ты...",
    2: "2️⃣ Что помогает тебе войти в \"рабочий поток\"?",
    3: "3️⃣ Что чаще всего мешает тебе сфокусироваться?",
    4: "4️⃣ Как ты обычно решаешь сложные задачи?",
    5: "5️⃣ Что для тебя признак настоящего фокуса?",
    6: "6️⃣ Когда ты чувствуешь себя продуктивнее всего?",
}

DIVIDER_TEXT = "💬 И последние 2 вопроса — чтобы мы лучше понимали, что тебе интересно 👇"

QUESTION_7 = "7️⃣ Интересна ли тебе альтернатива кофе и классическим энергетикам — напиток, который помогает фокусироваться без сахара и резких стимуляторов?"

QUESTION_8 = "8️⃣ Если ты уже попробовал(-а) High Focus, какой вкус тебе понравился больше всего?"

RESULTS = {
    "creative": """🚀 Класс! Ты прошёл квиз до конца — фокус точно на месте ⚡️

💡 Твой тип — Креативный фокус.
Ты мыслишь нестандартно, ловишь вдохновение из всего вокруг и умеешь соединять то, что другим кажется несовместимым.

🍐 Твой вкус High Focus — Груша–Пармезан.
Смелый, свежий и необычный — как твои идеи.""",
    
    "analytical": """🚀 Класс! Ты прошёл квиз до конца — фокус точно на месте ⚡️

🧠 Твой тип — Аналитический фокус.
Ты включаешься, когда нужно структурировать хаос и найти логику даже в креативе.

🍫 Твой вкус High Focus — Брауни.
Концентрация, глубина и точность — всё, как ты любишь.""",
    
    "energetic": """🚀 Класс! Ты прошёл квиз до конца — фокус точно на месте ⚡️

⚡️ Твой тип — Энергетический фокус.
Ты всегда в движении, задаёшь темп и заряжаешь всех вокруг.

🍯 Твой вкус High Focus — Солёная карамель.
Мягкий драйв и сила — идеальный баланс для твоего ритма."""
}

FINAL_TEXT = """Хочешь попробовать свой вкус прямо сейчас?
Подпишись на наш канал, покажи нам на стенде и получи подарок 🎁
А если уже дегустировал — приходи сыграть в наши активности и собери стикеры ⚡️"""

SUBSCRIBED_TEXT = """Отлично! 🎉

Приходи на наш стенд, покажи подписку и получи подарок 🎁
Увидимся! ⚡️"""

# Полные тексты ответов для сохранения в БД
ANSWER_TEXTS = {
    "q1_creative": "💡 Ищу вдохновение и новые подходы",
    "q1_analytical": "🧠 Раскладываю задачу по шагам",
    "q1_energetic": "⚡️ Просто начинаю делать — фокус приходит в действии",
    
    "q2_creative": "🎶 Настроение, музыка, атмосфера",
    "q2_analytical": "📋 Чёткий план и порядок",
    "q2_energetic": "🚀 Азарт, дедлайн и движение",
    
    "q3_creative": "💭 Однообразие, скука",
    "q3_analytical": "📱 Шум, уведомления, отвлекающие люди",
    "q3_energetic": "💤 Усталость и низкий уровень энергии",
    
    "q4_creative": "💡 Ищу нестандартное решение",
    "q4_analytical": "🧠 Разбиваю на части и иду по шагам",
    "q4_energetic": "⚡️ Беру и делаю — разберусь по пути",
    
    "q5_creative": "💡 Поток идей и вдохновение",
    "q5_analytical": "🧠 Чёткие мысли и контроль над процессом",
    "q5_energetic": "⚡️ Максимальная скорость и энергия",
    
    "q6_analytical": "🌅 Утром — когда всё только начинается",
    "q6_creative": "🌇 Днём — в потоке задач и общения",
    "q6_energetic": "🌙 Вечером / ночью — когда никто не мешает",
    
    "q7_yes_need": "⚡️ Да, это то, чего не хватает",
    "q7_maybe_taste": "☕️ Возможно, если вкус будет приятный",
    "q7_curious": "🤷 Интересно попробовать",
    "q7_no_coffee": "🚫 Нет, я остаюсь при кофе",
    
    "q8_pear": "🍐 Груша–Пармезан",
    "q8_caramel": "🍯 Солёная карамель",
    "q8_brownie": "🍫 Брауни",
    "q8_want": "🤔 Ещё не пробовал, но хочу",
    "q8_undecided": "🤷 Пока не решил"
}


# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(START_TEXT, reply_markup=get_start_keyboard())


# Обработчик кнопки "Назад"
@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(START_TEXT, reply_markup=get_start_keyboard())
    await callback.answer()


# Обработчик кнопки "Что за High Focus?"
@dp.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.answer(ABOUT_TEXT, reply_markup=get_back_to_start_keyboard())
    await callback.answer()


# Обработчик начала квиза
@dp.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.question_1)
    await state.update_data(answers={})
    await callback.message.answer(QUESTIONS[1], reply_markup=get_question_1_keyboard())
    await callback.answer()


# Обработчик вопроса 1
@dp.callback_query(QuizStates.question_1, F.data.startswith("q1_"))
async def process_question_1(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q1"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_2)
    await callback.message.answer(QUESTIONS[2], reply_markup=get_question_2_keyboard())
    await callback.answer()


# Обработчик вопроса 2
@dp.callback_query(QuizStates.question_2, F.data.startswith("q2_"))
async def process_question_2(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q2"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_3)
    await callback.message.answer(QUESTIONS[3], reply_markup=get_question_3_keyboard())
    await callback.answer()


# Обработчик вопроса 3
@dp.callback_query(QuizStates.question_3, F.data.startswith("q3_"))
async def process_question_3(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q3"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_4)
    await callback.message.answer(QUESTIONS[4], reply_markup=get_question_4_keyboard())
    await callback.answer()


# Обработчик вопроса 4
@dp.callback_query(QuizStates.question_4, F.data.startswith("q4_"))
async def process_question_4(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q4"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_5)
    await callback.message.answer(QUESTIONS[5], reply_markup=get_question_5_keyboard())
    await callback.answer()


# Обработчик вопроса 5
@dp.callback_query(QuizStates.question_5, F.data.startswith("q5_"))
async def process_question_5(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q5"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_6)
    await callback.message.answer(QUESTIONS[6], reply_markup=get_question_6_keyboard())
    await callback.answer()


# Обработчик вопроса 6
@dp.callback_query(QuizStates.question_6, F.data.startswith("q6_"))
async def process_question_6(callback: CallbackQuery, state: FSMContext):
    focus_type = callback.data.split("_")[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q6"] = {
        "type": focus_type,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    # Показываем разделитель
    await callback.message.answer(DIVIDER_TEXT)
    await asyncio.sleep(1.5)
    
    await state.set_state(QuizStates.question_7)
    await callback.message.answer(QUESTION_7, reply_markup=get_question_7_keyboard())
    await callback.answer()


# Обработчик вопроса 7
@dp.callback_query(QuizStates.question_7, F.data.startswith("q7_"))
async def process_question_7(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_", 1)[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q7"] = {
        "type": answer,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    await state.update_data(answers=answers)
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    await state.set_state(QuizStates.question_8)
    await callback.message.answer(QUESTION_8, reply_markup=get_question_8_keyboard())
    await callback.answer()


# Обработчик вопроса 8 и показ результатов
@dp.callback_query(QuizStates.question_8, F.data.startswith("q8_"))
async def process_question_8(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_", 1)[1]
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q8"] = {
        "type": answer,
        "text": ANSWER_TEXTS.get(callback.data, callback.data)
    }
    
    # Убираем кнопки у предыдущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Показываем выбранный ответ как сообщение от пользователя
    selected_answer = ANSWER_TEXTS.get(callback.data, callback.data)
    await callback.message.answer(f"👤 {selected_answer}")
    
    # Подсчитываем результаты (вопросы 1-6)
    focus_counts = {"creative": 0, "analytical": 0, "energetic": 0}
    for i in range(1, 7):
        answer_data = answers.get(f"q{i}")
        if answer_data and isinstance(answer_data, dict):
            focus_type = answer_data.get("type")
            if focus_type in focus_counts:
                focus_counts[focus_type] += 1
    
    # Определяем доминирующий тип фокуса
    dominant_focus = max(focus_counts, key=focus_counts.get)
    
    # Сохраняем результаты в БД
    await db.save_quiz_result(
        user_id=callback.from_user.id,
        focus_type=dominant_focus,
        answers=answers
    )
    
    # Показываем результат
    result_text = RESULTS[dominant_focus]
    await callback.message.answer(result_text)
    await asyncio.sleep(2)
    
    # Показываем финальное сообщение
    await callback.message.answer(FINAL_TEXT, reply_markup=get_final_keyboard())
    await state.clear()
    await callback.answer()


# Обработчик кнопки "Уже подписан"
@dp.callback_query(F.data == "already_subscribed")
async def already_subscribed(callback: CallbackQuery):
    await callback.message.answer(SUBSCRIBED_TEXT)
    await callback.answer("Спасибо! 🎉")


# Служебная команда для получения Telegram ID
@dp.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


# Админ-команда: перезапуск сервиса (для Railway/Fly.io и прочих PaaS)
@dp.message(Command(commands=["redeploy", "restart"]))
async def admin_redeploy(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("⛔️ Команда доступна только администраторам. Настрой ADMIN_IDS в переменных окружения.")
        return
    await message.answer("♻️ Перезапускаю сервис... Бот будет недоступен 3-5 секунд.")

    async def _exit_later():
        await asyncio.sleep(1)
        # Завершаем процесс с кодом 1, чтобы платформа перезапустила контейнер
        _os._exit(1)

    asyncio.create_task(_exit_later())


# Help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Доступные команды:\n/start — начать\n/whoami — ваш Telegram ID\n/redeploy — перезапуск (только для админов)")


# Fallback для неизвестных команд
@dp.message(F.text.regexp(r"^/"))
async def unknown_command(message: Message):
    await message.answer("Команда не найдена. Попробуйте /help")


async def main():
    # Инициализация БД
    await db.init_db()
    logger.info("База данных инициализирована")
    
    # Запуск бота
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

