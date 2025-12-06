import asyncio
import logging
import os
import os as _os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database_postgres import Database
from states import QuizStates
from keyboards import (
    get_start_keyboard,
    get_back_to_start_keyboard,
    get_consent_keyboard,
    get_question_1_keyboard,
    get_question_2_keyboard,
    get_question_3_keyboard,
    get_question_4_keyboard,
    get_question_5_keyboard,
    get_highfocus_q1_keyboard,
    get_highfocus_q2_keyboard,
    get_highfocus_q3_keyboard,
    get_final_keyboard
)
from consent_text import CONSENT_SHORT, CONSENT_FULL

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация базы данных PostgreSQL
db = Database()

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

Хочешь узнать, какой у тебя **тип фокуса** — и какой **вкус** High Focus включает тебя на максимум? ⚡️

🧠 Квиз основан на исследовании нейропсихиатора Дэниела Амена, выделяющем 7 типов работы мозга в стрессе, энергии и выгорании."""

ABOUT_TEXT = """High Focus — это инновационный молочный напиток от ЭкоНивы, созданный для тех, кто работает головой.

В составе:
☕️ гуарана — мягкая энергия,
🍃 L-теанин — концентрация и баланс,
💊 витамины группы B — поддержка мозга и настроения.

Без сахарозы. Без лактозы. Только чистый фокус и энергия."""

FOCUS_INTRO = """Основные вопросы про фокус (с типами ответов)

Основано на исследовании нейропсихиатора Дэниела Амена, выделяющем 7 типов работы мозга в стрессе, энергии и выгорании."""

QUESTIONS = {
    1: "1️⃣ Как вы реагируете на срочный дедлайн?",
    2: "2️⃣ Что помогает вам включиться в сложную задачу?",
    3: "3️⃣ Как вы чувствуете приближение выгорания?",
    4: "4️⃣ Что вас больше всего истощает в долгом проекте?",
    5: "5️⃣ Как вы восстанавливаетесь после стресса?",
}

RESULTS = {
    "compulsive": """🔒 Компульсивный тип 

Вы собраны, структурны и цените контроль. Ваш мозг работает лучше, когда всё по плану.

💡 Рекомендуемый вкус: 🍫 Брауни — глубокий, устойчивый, помогает сохранять фокус и внутренний порядок.""",
    
    "anxious": """😰 Тревожный тип

Вы стремитесь к предсказуемости и спокойствию, но часто переоцениваете риски.

💡 Рекомендуемый вкус: 🍯 Солёная карамель — баланс сладости и лёгкой соли помогает удерживать гармонию и снижает внутреннее напряжение.""",
    
    "depressive": """😔 Депрессивный тип

Вы чувствительны к рутине и теряете энергию, если нет вдохновения.

💡 Рекомендуемый вкус: 🍐 Груша–Пармезан — мягкое, но пробуждающее сочетание, возвращающее интерес и тонус.""",
    
    "impulsive": """🌋 Вспыльчивый тип

Вы энергичны и реактивны, быстро включаетесь, но также быстро вспыхиваете.

💡 Рекомендуемый вкус: 🍯 Солёная карамель — сочетает мягкость и лёгкую «остринку», помогая выпускать энергию осознанно.""",
    
    "hyperactive": """⚡ Импульсивный тип

Вы ищете драйв, новизну и мгновенный результат.

💡 Рекомендуемый вкус: 🍐 Груша–Пармезан — сложный, многослойный, удерживает интерес и направляет энергию в нужное русло.""",
    
    "cyclothymic": """🎭 Циклотимный тип

Ваше настроение и энергия меняются волнами, вы остро чувствуете всё происходящее.

💡 Рекомендуемый вкус: 🍐 Груша–Пармезан — отражает вашу многогранность и помогает мягко стабилизировать эмоциональный фон.""",
    
    "balanced": """☯ Сбалансированный тип

Вы устойчивы, гибко адаптируетесь и чувствуете внутреннюю гармонию.

💡 Рекомендуемый вкус: 🧃 Вне зависимости от вкуса, вам подойдёт любой High Focus — попробуйте все, чтобы выбрать свой идеальный баланс."""
}

SUBSCRIPTION_TEXT = """⚡️ Остался последний шаг — подпишись на наш Telegram-канал High Focus!

Там — всё о концентрации, энергии и продуктивности: как оставаться в фокусе, когда мир шумит, и как прокачивать себя каждый день."""

# Дополнительные вопросы о High Focus
HIGHFOCUS_INTRO = """Перед финалом — пара вопросов о High Focus, чтобы понимать, что ты в теме 😎🤝"""

HIGHFOCUS_Q1 = """1️⃣ High Focus — это…

Выбери вариант, который лучше всего описывает наш продукт 👇"""

HIGHFOCUS_Q2 = """2️⃣ А теперь про эффект.

Зачем вообще пить High Focus?"""

HIGHFOCUS_Q3 = """3️⃣ В какой ситуации High Focus подходит лучше всего?"""

# Правильные ответы High Focus
HIGHFOCUS_CORRECT_Q1 = "✅ Отлично! Ты правильно уловил суть High Focus — двигаемся дальше ⚡️"
HIGHFOCUS_CORRECT_Q2 = "✅ Да! С таким фокусом по жизни далеко уйдёшь 😉\n\nПоехали дальше!"
HIGHFOCUS_CORRECT_Q3 = "✅ Точно в цель! Ты отлично чувствуешь, когда нужен High Focus 🎯"

# Неправильные ответы High Focus
HIGHFOCUS_WRONG_Q1 = {
    "🥤 Новый энергетик на основе молока Эконива": "❌ Похоже, фокус чуть сместился.\n\nHigh Focus не относится к энергетикам — мы работаем совсем иначе.\n\nДавай попробуем ещё раз 👇",
    "☕️ Кофейный напиток для бодрости и энергии": "❌ Немного мимо.\n\nHigh Focus — это не кофе, и эффект у нас тоже другой.\n\nПопробуем ещё раз 👇"
}

HIGHFOCUS_WRONG_Q2 = {
    "😵 Чтобы взбодриться и «врубить турбо-режим»": "❌ Улетели слишком далеко 😅\n\nHigh Focus — не про жёсткий \"турбо-режим\", а про более осознанное состояние.\n\nДавай попробуем ещё раз 👇",
    "🚀 Чтобы резко поднять энергию, как у энергетиков": "❌ Немного не то.\n\nHigh Focus не работает как классический энергетик с резким скачком.\n\nПопробуем ещё раз 👇"
}

HIGHFOCUS_WRONG_Q3 = {
    "😵 Когда нужно бодрствовать всю ночь": "❌ Это уже задача для супергероев 😅\n\nHigh Focus — не для ночных марафонов без сна.\n\nДавай попробуем ещё раз 👇",
    "🍔 Когда хочешь заменить приём пищи": "❌ Мы точно не про это!\n\nHigh Focus не заменяет еду — он про ум и концентрацию.\n\nПопробуем ещё раз 👇"
}

# Полные тексты ответов для сохранения в БД
ANSWER_TEXTS = {
    "q1_compulsive": "А) Быстро собираюсь, делаю план и иду по нему. (🔒 Компульсивный)",
    "q1_anxious": "Б) Начинаю тревожиться и прокручивать негативные сценарии. (😰 Тревожный)",
    "q1_depressive": "В) Чувствую упадок и прокрастинирую. (😔 Депрессивный)",
    "q1_impulsive": "Г) Заряжаюсь энергией, но могу вспылить. (🌋 Вспыльчивый)",
    "q1_hyperactive": "Д) Бросаюсь в задачу с азартом, но хаотично. (⚡ Импульсивный)",
    "q1_cyclothymic": "Е) То включаюсь, то выгораю — скачки энергии. (🎭 Циклотимный)",
    "q1_balanced": "Ж) Спокойно адаптируюсь, распределяю силы. (☯ Сбалансированный)",
    
    "q2_compulsive": "А) План и контроль. (🔒)",
    "q2_anxious": "Б) Уверенность, что всё под контролем. (😰)",
    "q2_depressive": "В) Поддержка и признание. (😔)",
    "q2_impulsive": "Г) Азарт и драйв. (🌋)",
    "q2_hyperactive": "Д) Новизна и вызов. (⚡)",
    "q2_cyclothymic": "Е) Вдохновение и увлечённость. (🎭)",
    "q2_balanced": "Ж) Баланс интереса и пользы. (☯)",
    
    "q3_compulsive": "А) Всё раздражает, если что-то идёт не по плану. (🔒)",
    "q3_anxious": "Б) Не могу отключить тревожные мысли. (😰)",
    "q3_depressive": "В) Пустота и апатия. (😔)",
    "q3_impulsive": "Г) Вспышки гнева по мелочам. (🌋)",
    "q3_hyperactive": "Д) Теряю интерес, ищу острые ощущения. (⚡)",
    "q3_cyclothymic": "Е) Настроение скачет. (🎭)",
    "q3_balanced": "Ж) Постоянная усталость, даже после отдыха. (☯)",
    
    "q4_compulsive": "А) Хаос и постоянные изменения. (🔒)",
    "q4_anxious": "Б) Неопределенность и риски. (😰)",
    "q4_depressive": "В) Рутина и отсутствие смысла. (😔)",
    "q4_impulsive": "Г) Необходимость сдерживать эмоции. (🌋)",
    "q4_hyperactive": "Д) Монотонность без быстрых побед. (⚡)",
    "q4_cyclothymic": "Е) Конфликты и негативная атмосфера. (🎭)",
    "q4_balanced": "Ж) Нет времени на восстановление. (☯)",
    
    "q5_compulsive": "А) Навожу порядок, планирую. (🔒)",
    "q5_anxious": "Б) Ухожу в спокойную рутину. (😰)",
    "q5_depressive": "В) Уединяюсь в тишине. (😔)",
    "q5_impulsive": "Г) Выплескиваю эмоции через спорт или музыку. (🌋)",
    "q5_hyperactive": "Д) Меняю обстановку, ищу новое. (⚡)",
    "q5_cyclothymic": "Е) Провожу время с близкими. (🎭)",
    "q5_balanced": "Ж) Сон, еда, хобби, баланс. (☯)"
}

# Маппинг текстов ответов на типы фокуса (для обработки text messages)
TEXT_TO_TYPE = {
    # Вопрос 1
    "А) Быстро собираюсь, делаю план и иду по нему. (🔒 Компульсивный)": "compulsive",
    "Б) Начинаю тревожиться и прокручивать негативные сценарии. (😰 Тревожный)": "anxious",
    "В) Чувствую упадок и прокрастинирую. (😔 Депрессивный)": "depressive",
    "Г) Заряжаюсь энергией, но могу вспылить. (🌋 Вспыльчивый)": "impulsive",
    "Д) Бросаюсь в задачу с азартом, но хаотично. (⚡ Импульсивный)": "hyperactive",
    "Е) То включаюсь, то выгораю — скачки энергии. (🎭 Циклотимный)": "cyclothymic",
    "Ж) Спокойно адаптируюсь, распределяю силы. (☯ Сбалансированный)": "balanced",
    
    # Вопрос 2
    "А) План и контроль. (🔒)": "compulsive",
    "Б) Уверенность, что всё под контролем. (😰)": "anxious",
    "В) Поддержка и признание. (😔)": "depressive",
    "Г) Азарт и драйв. (🌋)": "impulsive",
    "Д) Новизна и вызов. (⚡)": "hyperactive",
    "Е) Вдохновение и увлечённость. (🎭)": "cyclothymic",
    "Ж) Баланс интереса и пользы. (☯)": "balanced",
    
    # Вопрос 3
    "А) Всё раздражает, если что-то идёт не по плану. (🔒)": "compulsive",
    "Б) Не могу отключить тревожные мысли. (😰)": "anxious",
    "В) Пустота и апатия. (😔)": "depressive",
    "Г) Вспышки гнева по мелочам. (🌋)": "impulsive",
    "Д) Теряю интерес, ищу острые ощущения. (⚡)": "hyperactive",
    "Е) Настроение скачет. (🎭)": "cyclothymic",
    "Ж) Постоянная усталость, даже после отдыха. (☯)": "balanced",
    
    # Вопрос 4
    "А) Хаос и постоянные изменения. (🔒)": "compulsive",
    "Б) Неопределенность и риски. (😰)": "anxious",
    "В) Рутина и отсутствие смысла. (😔)": "depressive",
    "Г) Необходимость сдерживать эмоции. (🌋)": "impulsive",
    "Д) Монотонность без быстрых побед. (⚡)": "hyperactive",
    "Е) Конфликты и негативная атмосфера. (🎭)": "cyclothymic",
    "Ж) Нет времени на восстановление. (☯)": "balanced",
    
    # Вопрос 5
    "А) Навожу порядок, планирую. (🔒)": "compulsive",
    "Б) Ухожу в спокойную рутину. (😰)": "anxious",
    "В) Уединяюсь в тишине. (😔)": "depressive",
    "Г) Выплескиваю эмоции через спорт или музыку. (🌋)": "impulsive",
    "Д) Меняю обстановку, ищу новое. (⚡)": "hyperactive",
    "Е) Провожу время с близкими. (🎭)": "cyclothymic",
    "Ж) Сон, еда, хобби, баланс. (☯)": "balanced"
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
    await message.answer(START_TEXT, reply_markup=get_start_keyboard(), parse_mode="Markdown")


# Обработчик кнопки "Назад"
@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(START_TEXT, reply_markup=get_start_keyboard(), parse_mode="Markdown")
    await callback.answer()


# Обработчик кнопки "Что за High Focus?"
@dp.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.answer(ABOUT_TEXT, reply_markup=get_back_to_start_keyboard())
    await callback.answer()


# Обработчик начала квиза
@dp.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """Показ формы согласия на обработку персональных данных"""
    await state.set_state(QuizStates.consent)
    
    # Отправляем файл с политикой обработки данных
    consent_file = FSInputFile("Политика_обработки_персональных_данных.docx")
    await callback.message.answer_document(
        consent_file,
        caption="📄 Политика обработки персональных данных\n\nПожалуйста, ознакомьтесь с документом.",
        reply_markup=get_consent_keyboard()
    )
    await callback.answer()


# Обработчик согласия
@dp.callback_query(QuizStates.consent, F.data == "consent_agree")
async def process_consent_agree(callback: CallbackQuery, state: FSMContext):
    """Пользователь согласился с обработкой данных"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("👤 Согласен")
    
    # Сохраняем согласие в данные состояния
    await state.update_data(consent_given=True, answers={})
    
    # Переходим к первому вопросу
    await state.set_state(QuizStates.question_1)
    await callback.message.answer(FOCUS_INTRO)
    await callback.message.answer(QUESTIONS[1], reply_markup=get_question_1_keyboard())
    await callback.answer()


@dp.callback_query(QuizStates.consent, F.data == "consent_disagree")
async def process_consent_disagree(callback: CallbackQuery, state: FSMContext):
    """Пользователь не согласился с обработкой данных"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("👤 Не согласен")
    
    await callback.message.answer(
        "😔 Без согласия на обработку данных мы не можем провести квиз.\n\n"
        "Если передумаете — возвращайтесь! 👋",
        reply_markup=get_start_keyboard()
    )
    await state.clear()
    await callback.answer()


# Обработчик вопроса 1
@dp.message(QuizStates.question_1, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_1(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q1"] = {
        "type": focus_type,
        "text": message.text
    }
    await state.update_data(answers=answers)
    
    await state.set_state(QuizStates.question_2)
    await message.answer(QUESTIONS[2], reply_markup=get_question_2_keyboard())


# Обработчик вопроса 2
@dp.message(QuizStates.question_2, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_2(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q2"] = {
        "type": focus_type,
        "text": message.text
    }
    await state.update_data(answers=answers)
    
    await state.set_state(QuizStates.question_3)
    await message.answer(QUESTIONS[3], reply_markup=get_question_3_keyboard())


# Обработчик вопроса 3
@dp.message(QuizStates.question_3, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_3(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q3"] = {"type": focus_type, "text": message.text}
    await state.update_data(answers=answers)
    
    await state.set_state(QuizStates.question_4)
    await message.answer(QUESTIONS[4], reply_markup=get_question_4_keyboard())


# Обработчик вопроса 4
@dp.message(QuizStates.question_4, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_4(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q4"] = {"type": focus_type, "text": message.text}
    await state.update_data(answers=answers)
    
    await state.set_state(QuizStates.question_5)
    await message.answer(QUESTIONS[5], reply_markup=get_question_5_keyboard())


# Обработчик вопроса 5 - переход к дополнительным вопросам о High Focus
@dp.message(QuizStates.question_5, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_5(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q5"] = {"type": focus_type, "text": message.text}
    
    # Подсчитываем результаты (все 5 вопросов)
    type_counts = {
        "compulsive": 0,
        "anxious": 0,
        "depressive": 0,
        "impulsive": 0,
        "hyperactive": 0,
        "cyclothymic": 0,
        "balanced": 0
    }
    
    for i in range(1, 6):
        answer_data = answers.get(f"q{i}")
        if answer_data and isinstance(answer_data, dict):
            brain_type = answer_data.get("type")
            if brain_type in type_counts:
                type_counts[brain_type] += 1
    
    # Определяем доминирующий тип мозга
    dominant_type = max(type_counts, key=type_counts.get)
    
    # Сохраняем результат в state для показа после всех вопросов
    await state.update_data(
        quiz_result=dominant_type, 
        answers=answers,
        highfocus_wrong={"q1": [], "q2": [], "q3": []}  # Массивы для неправильных ответов
    )
    
    # Переходим к дополнительным вопросам о High Focus
    await asyncio.sleep(1)
    await message.answer(HIGHFOCUS_INTRO)
    await asyncio.sleep(1.5)
    
    await state.set_state(QuizStates.highfocus_q1)
    await message.answer(HIGHFOCUS_Q1, reply_markup=get_highfocus_q1_keyboard())


# Обработчик High Focus вопрос 1
@dp.message(QuizStates.highfocus_q1)
async def process_highfocus_q1(message: Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    answers = data.get("answers", {})
    highfocus_wrong = data.get("highfocus_wrong", {"q1": [], "q2": [], "q3": []})
    
    # Проверяем правильный ответ
    is_correct = (answer == "🧠 Молочный напиток для концентрации и энергии на основе гуараны и L-теанина")
    
    if is_correct:
        # Сохраняем правильный ответ
        answers["highfocus_q1"] = {"text": answer, "is_correct": True}
        await state.update_data(answers=answers, highfocus_wrong=highfocus_wrong)
        
        await message.answer(HIGHFOCUS_CORRECT_Q1)
        await asyncio.sleep(1.5)
        
        await state.set_state(QuizStates.highfocus_q2)
        await message.answer(HIGHFOCUS_Q2, reply_markup=get_highfocus_q2_keyboard())
    else:
        # Сохраняем неправильный ответ
        highfocus_wrong["q1"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
        # Показываем сообщение об ошибке и спрашиваем заново
        error_msg = HIGHFOCUS_WRONG_Q1.get(answer, "❌ Попробуем ещё раз 👇")
        await message.answer(error_msg)
        await asyncio.sleep(1.5)
        await message.answer(HIGHFOCUS_Q1, reply_markup=get_highfocus_q1_keyboard())


# Обработчик High Focus вопрос 2
@dp.message(QuizStates.highfocus_q2)
async def process_highfocus_q2(message: Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    answers = data.get("answers", {})
    highfocus_wrong = data.get("highfocus_wrong", {"q1": [], "q2": [], "q3": []})
    
    # Проверяем правильный ответ
    is_correct = (answer == "🧠 Чтобы поддерживать концентрацию, ясность и мягкий уровень энергии в течение дня")
    
    if is_correct:
        # Сохраняем правильный ответ
        answers["highfocus_q2"] = {"text": answer, "is_correct": True}
        await state.update_data(answers=answers, highfocus_wrong=highfocus_wrong)
        
        await message.answer(HIGHFOCUS_CORRECT_Q2)
        await asyncio.sleep(1.5)
        
        await state.set_state(QuizStates.highfocus_q3)
        await message.answer(HIGHFOCUS_Q3, reply_markup=get_highfocus_q3_keyboard())
    else:
        # Сохраняем неправильный ответ
        highfocus_wrong["q2"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
        # Показываем сообщение об ошибке
        error_msg = HIGHFOCUS_WRONG_Q2.get(answer, "❌ Попробуем ещё раз 👇")
        await message.answer(error_msg)
        await asyncio.sleep(1.5)
        await message.answer(HIGHFOCUS_Q2, reply_markup=get_highfocus_q2_keyboard())


# Обработчик High Focus вопрос 3 - финальный переход к результатам
@dp.message(QuizStates.highfocus_q3)
async def process_highfocus_q3(message: Message, state: FSMContext):
    from aiogram.types import ReplyKeyboardRemove
    
    answer = message.text
    data = await state.get_data()
    answers = data.get("answers", {})
    highfocus_wrong = data.get("highfocus_wrong", {"q1": [], "q2": [], "q3": []})
    
    # Проверяем правильный ответ
    is_correct = (answer == "📚 Когда нужно включить голову, сосредоточиться и работать внимательно")
    
    if is_correct:
        # Сохраняем правильный ответ
        answers["highfocus_q3"] = {"text": answer, "is_correct": True}
        
        # Добавляем информацию о неправильных ответах и попытках
        answers["highfocus_attempts"] = {
            "q1": {"wrong_answers": highfocus_wrong.get("q1", []), "attempts": len(highfocus_wrong.get("q1", [])) + 1},
            "q2": {"wrong_answers": highfocus_wrong.get("q2", []), "attempts": len(highfocus_wrong.get("q2", [])) + 1},
            "q3": {"wrong_answers": highfocus_wrong.get("q3", []), "attempts": len(highfocus_wrong.get("q3", [])) + 1}
        }
        
        await message.answer(HIGHFOCUS_CORRECT_Q3)
        await asyncio.sleep(1.5)
        
        # Сохраняем ВСЕ данные в quiz_results (включая неправильные ответы)
        quiz_result = data.get("quiz_result")
        
        try:
            await db.save_quiz_result(
                user_id=message.from_user.id,
                focus_type=quiz_result,
                answers=answers
            )
            logger.info(f"Сохранено полное прохождение квиза для user {message.from_user.id}")
        except Exception as e:
            # Логируем ошибку, но не падаем
            logger.error(f"Ошибка сохранения в БД для user {message.from_user.id}: {e}", exc_info=True)
        
        # Сохраняем обновленные данные в state
        await state.update_data(answers=answers)
        
        # Удаляем reply keyboard
        await message.answer("✅", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.5)
        
        # Показываем сообщение о подписке с кнопками
        await message.answer(SUBSCRIPTION_TEXT, reply_markup=get_final_keyboard())
    else:
        # Сохраняем неправильный ответ
        highfocus_wrong["q3"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
        # Показываем сообщение об ошибке
        error_msg = HIGHFOCUS_WRONG_Q3.get(answer, "❌ Попробуем ещё раз 👇")
        await message.answer(error_msg)
        await asyncio.sleep(1.5)
        await message.answer(HIGHFOCUS_Q3, reply_markup=get_highfocus_q3_keyboard())


# Обработчик кнопки "Уже подписан"
@dp.callback_query(F.data == "already_subscribed")
async def already_subscribed(callback: CallbackQuery, state: FSMContext):
    # Получаем результат квиза из state
    data = await state.get_data()
    quiz_result = data.get("quiz_result")
    
    if quiz_result:
        # Показываем результат квиза
        result_text = RESULTS[quiz_result]
        await callback.message.answer(result_text)
    
    await callback.answer("Спасибо! 🎉")
    
    # Очищаем state
    await state.clear()


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
    try:
        # Инициализация БД
        await db.init_db()
        logger.info("База данных PostgreSQL инициализирована")
        
        # Запуск бота
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())

