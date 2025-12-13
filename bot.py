import asyncio
import logging
import os
import os as _os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
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

# ========== ТЕКСТЫ ==========

START_TEXT = """⚡️ Привет! Это High Focus — напиток для тех, кто работает головой.

High Focus создан, чтобы помогать сохранять концентрацию и энергию в мире, где информации больше, чем времени.

Хочешь узнать, какой у тебя тип концентрации и какой вкус High Focus выбрать? ⚡️"""

ABOUT_TEXT = """High Focus — это инновационный молочный напиток от «ЭкоНивы», созданный для концентрации внимания и повышения энергии.

В составе:

☕️ Гуарана — заряжает энергией и повышает работоспособность

🍃 L-теанин — помогает сконцентрироваться и направляет энергию на достижение цели

💊 Витамины группы B — участвуют в синтезе энергии, укрепляют иммунитет

Без сахарозы. Без лактозы. Только чистые концентрация и энергия."""

FOCUS_INTRO = """🧠 Тест основан на исследовании нейропсихиатра Дэниэла Дж. Амена, выделяющего 7 типов работы мозга при стрессе и выгорании."""

QUESTIONS = {
    1: "1️⃣ Как вы реагируете на срочный дедлайн?",
    2: "2️⃣ Что помогает вам включиться в сложную задачу?",
    3: "3️⃣ Как вы чувствуете приближение выгорания?",
    4: "4️⃣ Что вас истощает сильнее всего в долгом проекте?",
    5: "5️⃣ Как вы восстанавливаетесь после стресса?",
}

# ========== РЕЗУЛЬТАТЫ (5 типов) ==========

RESULTS = {
    "persistent": """🧠 Настойчивый тип

Вы собраны, упорны, цените контроль и порядок. Ваш мозг работает на максимуме, когда всё идёт по плану.

💡 Рекомендуемый вкус: 🍫 «Брауни» — глубокий, устойчивый вкус помогает сохранять концентрацию и наводить порядок в делах.""",
    
    "spontaneous": """⚡️ Спонтанный тип

Вы энергичны, креативны и ищете драйв. Рутина — ваш главный враг, а новизна — топливо.

💡 Рекомендуемый вкус: 🍐 «Груша и пармезан» — неожиданное, многогранное сочетание удержит ваш интерес и направит энергию в конструктивное русло.""",
    
    "cautious": """🛡 Осторожный тип

Вы предусмотрительны и ответственны, но склонны к излишнему беспокойству. Вам важна безопасность и предсказуемость.

💡 Рекомендуемый вкус: 🍯 «Солёная карамель» — баланс сладости и солёности помогает удерживать внутреннюю гармонию и снижает напряжение.""",
    
    "sensitive": """🎨 Чувствительный тип

Вы — человек настроения. Ваша концентрация и энергия тесно связаны с тем, что происходит внутри. Вы глубоко чувствующий, творческий и эмпатичный, но легко перегружаетесь. Вам важно, чтобы всё было «в резонансе».

💡 Рекомендуемый вкус: выбирайте вкус по настроению 

😔 Нужен комфорт и поддержка → 🍯 «Солёная карамель»
💡 Хочу вдохновения и новизны → 🍐 «Груша и пармезан»
🧱 Помочь с фокусом и структурой → 🍫 «Брауни»""",
    
    "balanced": """☯️ Сбалансированный тип

Вы устойчивы, гибки и адаптивны. Умеете распределять силы и находить гармонию между работой и отдыхом.

💡 Рекомендуемый вкус: 🧃 Вам подойдёт любой! Ваша сила — в умении подстраиваться. Попробуйте все варианты, чтобы выбрать самый приятный спутник для вашей продуктивности."""
}

# ========== ИЗОБРАЖЕНИЯ ==========

# Картинки типов фокуса
FOCUS_TYPE_IMAGES = {
    "persistent": "Frame 49.png",   # Настойчивый
    "spontaneous": "Frame 47.png",  # Спонтанный
    "cautious": "Frame 31.png",     # Осторожный
    "sensitive": "Frame 50.png",    # Чувствительный
    "balanced": "Frame 29.png",     # Сбалансированный
}

# Картинки вкусов
FLAVOR_IMAGES = {
    "persistent": "Frame 44.png",   # Брауни
    "spontaneous": "Frame 43.png",  # Груша-Пармезан
    "cautious": "Frame 45.png",     # Солёная карамель
    "sensitive": "Frame 28.png",    # Все вкусы (для чувствительного — по настроению)
    "balanced": "Frame 28.png",     # Все вкусы
}

SUBSCRIPTION_TEXT = """Хочешь попробовать High Focus прямо сейчас?

Подпишись на наш канал, покажи нам на стенде это сообщение и получи подарок. 🎁

А если уже пробовал, приходи поучаствовать в наших активностях и собери стикеры. ⚡️"""

# ========== Вопросы о High Focus ==========

HIGHFOCUS_INTRO = """Перед финалом — пара вопросов о High Focus, чтобы понимать, что ты в теме 😎🤝"""

HIGHFOCUS_Q1 = """1️⃣ High Focus — это…

Выбери вариант, который лучше всего описывает наш продукт 👇"""

HIGHFOCUS_Q2 = """2️⃣ Зачем пить High Focus?"""

HIGHFOCUS_Q3 = """3️⃣ В какой ситуации High Focus подходит лучше всего?"""

# Правильные ответы High Focus
HIGHFOCUS_CORRECT_Q1 = "✅ Отлично! Ты правильно уловил суть High Focus — двигаемся дальше. ⚡️"
HIGHFOCUS_CORRECT_Q2 = "✅ Да! С таким фокусом по жизни далеко пойдешь. 😉\n\nПоехали дальше!"
HIGHFOCUS_CORRECT_Q3 = "✅ Точно в цель! Ты отлично чувствуешь, когда нужен High Focus. 🎯"

# Неправильные ответы High Focus
HIGHFOCUS_WRONG_Q1 = {
    "🥤 Новый энергетик на основе молока «ЭкоНива»": "❌ Похоже, фокус чуть сместился\n\nHigh Focus не относится к энергетикам — мы работаем совсем иначе.\n\nДавай попробуем еще раз. 👇",
    "☕️ Кофейный напиток для бодрости и энергии": "❌ Не попал\n\nHigh Focus — это не кофе, и эффект у него тоже другой.\n\nПопробуем еще раз. 👇"
}

HIGHFOCUS_WRONG_Q2 = {
    "😵 Чтобы взбодриться и «включить турборежим»": "❌ Улетели слишком далеко 😅\n\nHigh Focus не про жесткий «турборежим», а про более осознанное состояние.\n\nДавай попробуем еще раз. 👇",
    "🚀 Чтобы резко поднять энергию, как у энергетиков": "❌ Немного не то\n\nHigh Focus не работает как классический энергетик с резким скачком энергии и таким же резким спадом через время.\n\nПопробуем еще раз. 👇"
}

HIGHFOCUS_WRONG_Q3 = {
    "😵 Когда нужно бодрствовать всю ночь": "❌ Это уже задача для супергероев 😅\n\nHigh Focus не для ночных марафонов без сна.\n\nДавай попробуем еще раз. 👇",
    "🍔 Когда хочешь заменить приём пищи": "❌ Мы точно не про это!\n\nHigh Focus не заменяет еду — он дает энергию для концентрации.\n\nПопробуем еще раз. 👇"
}

# ========== Маппинг ответов на типы (5 типов) ==========

TEXT_TO_TYPE = {
    # Вопрос 1: Как вы реагируете на срочный дедлайн?
    "📋 Быстро составляю чёткий план и следую ему шаг за шагом": "persistent",
    "⚡️ Чувствую прилив драйва и азарта, но действую хаотично": "spontaneous",
    "😨 Тревожусь, прокручиваю в голове негативные сценарии": "cautious",
    "😔 Чувствую упадок сил, переживаю, что не справлюсь, прокрастинирую": "sensitive",
    "🧘‍♂️ Спокойно оцениваю объём, распределяю силы и приступаю": "balanced",
    
    # Вопрос 2: Что помогает вам включиться в сложную задачу?
    "📊 Чёткая структура, контрольный список и видение результата": "persistent",
    "🎯 Новизна, вызов, ощущение игры или соревнования": "spontaneous",
    "🛡️ Уверенность, что риски учтены, и есть запасной план": "cautious",
    "💡 Вдохновение, личная значимость и поддержка": "sensitive",
    "⚖️ Интерес к задаче и понимание её практической пользы": "balanced",
    
    # Вопрос 3: Как вы чувствуете приближение выгорания?
    "😤 Всё начинает раздражать, особенно неожиданности, даже если они приятные": "persistent",
    "🌀 Теряется интерес, настойчивое желание всё изменить": "spontaneous",
    "🚨 Не могу отключить навязчивые негативные тревожные мысли": "cautious",
    "🌫 Появляются пустота, апатия, всё теряет смысл": "sensitive",
    "🪫 Постоянная усталость, которая не проходит даже после отдыха": "balanced",
    
    # Вопрос 4: Что вас истощает сильнее всего в долгом проекте?
    "🌪 Хаос, постоянные изменения в требованиях и отсутствие порядка": "persistent",
    "🐌 Монотонность, рутина, отсутствие побед и вызовов": "spontaneous",
    "🎲 Неопределённость результата, высокие риски и отсутствие контроля над ситуацией": "cautious",
    "🔁 Механическая работа без личной вовлечённости и творчества": "sensitive",
    "⏳ Невозможность качественно восстанавливаться из-за плотного графика": "balanced",
    
    # Вопрос 5: Как вы восстанавливаетесь после стресса?
    "🧹 Навожу порядок в пространстве, составляю планы на будущее": "persistent",
    "🎪 Пробую что-то новое: место, хобби, активность. Ищу адреналин": "spontaneous",
    "🛌 Ухожу в тихую, спокойную рутину, минимизирую контакты": "cautious",
    "🎨 Уединяюсь, слушаю музыку, погружаюсь в творчество или природу": "sensitive",
    "🍃 Сон, хобби, общение, спорт — всё понемногу": "balanced"
}

# Финальное сообщение с промокодом
PROMO_MESSAGE_TEMPLATE = """🎉 Поздравляем! Ты выиграл промокод на скидку 30% для High Focus в Ozon!

Ты прошёл квиз и определил свой тип фокуса —
самое время попробовать High Focus в деле!

Твой персональный промокод на скидку: {promo_code}

👉 Купить High Focus на Ozon:
https://ozon.ru/t/T8vATiE

Промо-код действует до 31.12 и может быть использован только один раз."""

PROMO_EXHAUSTED_MESSAGE = """🎉 Поздравляем! Ты прошёл квиз и определил свой тип фокуса!

К сожалению, все промокоды закончились 😔

Но ты всё равно можешь попробовать High Focus:
👉 https://ozon.ru/t/T8vATiE"""


# ========== Загрузка промокодов при старте ==========

async def load_promo_codes():
    """Загрузка промокодов из CSV файла в БД"""
    promo_file = "promo_codes.csv"
    try:
        if os.path.exists(promo_file):
            with open(promo_file, "r") as f:
                codes = [line.strip() for line in f if line.strip()]
            await db.load_promo_codes_from_list(codes)
            logger.info(f"Загружено {len(codes)} промокодов из {promo_file}")
        else:
            logger.warning(f"Файл промокодов {promo_file} не найден")
    except Exception as e:
        logger.error(f"Ошибка загрузки промокодов: {e}", exc_info=True)


# ========== ОБРАБОТЧИКИ ==========

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(START_TEXT, reply_markup=get_start_keyboard(), parse_mode="Markdown")


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(START_TEXT, reply_markup=get_start_keyboard(), parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.answer(ABOUT_TEXT, reply_markup=get_back_to_start_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """Показ формы согласия на обработку персональных данных"""
    await state.set_state(QuizStates.consent)
    
    consent_file = FSInputFile("Политика_обработки_персональных_данных.docx")
    await callback.message.answer_document(
        consent_file,
        caption="📄 Политика обработки персональных данных\n\nПожалуйста, ознакомьтесь с документом.",
        reply_markup=get_consent_keyboard()
    )
    await callback.answer()


@dp.callback_query(QuizStates.consent, F.data == "consent_agree")
async def process_consent_agree(callback: CallbackQuery, state: FSMContext):
    """Пользователь согласился с обработкой данных"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("👤 Согласен")
    
    await state.update_data(consent_given=True, answers={})
    
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
    answers["q1"] = {"type": focus_type, "text": message.text}
    await state.update_data(answers=answers)
    
    await state.set_state(QuizStates.question_2)
    await message.answer(QUESTIONS[2], reply_markup=get_question_2_keyboard())


# Обработчик вопроса 2
@dp.message(QuizStates.question_2, F.text.in_(TEXT_TO_TYPE.keys()))
async def process_question_2(message: Message, state: FSMContext):
    focus_type = TEXT_TO_TYPE.get(message.text)
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q2"] = {"type": focus_type, "text": message.text}
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
        "persistent": 0,
        "spontaneous": 0,
        "cautious": 0,
        "sensitive": 0,
        "balanced": 0
    }
    
    for i in range(1, 6):
        answer_data = answers.get(f"q{i}")
        if answer_data and isinstance(answer_data, dict):
            brain_type = answer_data.get("type")
            if brain_type in type_counts:
                type_counts[brain_type] += 1
    
    # Определяем доминирующий тип
    dominant_type = max(type_counts, key=type_counts.get)
    
    await state.update_data(
        quiz_result=dominant_type, 
        answers=answers,
        highfocus_wrong={"q1": [], "q2": [], "q3": []}
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
    
    is_correct = (answer == "🧠 Молочный напиток для концентрации и энергии на основе гуараны и L-теанина")
    
    if is_correct:
        answers["highfocus_q1"] = {"text": answer, "is_correct": True}
        await state.update_data(answers=answers, highfocus_wrong=highfocus_wrong)
        
        await message.answer(HIGHFOCUS_CORRECT_Q1)
        await asyncio.sleep(1.5)
        
        await state.set_state(QuizStates.highfocus_q2)
        await message.answer(HIGHFOCUS_Q2, reply_markup=get_highfocus_q2_keyboard())
    else:
        highfocus_wrong["q1"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
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
    
    is_correct = (answer == "🧠 Чтобы поддерживать концентрацию, ясность и мягкий уровень энергии в течение дня")
    
    if is_correct:
        answers["highfocus_q2"] = {"text": answer, "is_correct": True}
        await state.update_data(answers=answers, highfocus_wrong=highfocus_wrong)
        
        await message.answer(HIGHFOCUS_CORRECT_Q2)
        await asyncio.sleep(1.5)
        
        await state.set_state(QuizStates.highfocus_q3)
        await message.answer(HIGHFOCUS_Q3, reply_markup=get_highfocus_q3_keyboard())
    else:
        highfocus_wrong["q2"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
        error_msg = HIGHFOCUS_WRONG_Q2.get(answer, "❌ Попробуем ещё раз 👇")
        await message.answer(error_msg)
        await asyncio.sleep(1.5)
        await message.answer(HIGHFOCUS_Q2, reply_markup=get_highfocus_q2_keyboard())


# Обработчик High Focus вопрос 3 - финальный переход к результатам
@dp.message(QuizStates.highfocus_q3)
async def process_highfocus_q3(message: Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    answers = data.get("answers", {})
    highfocus_wrong = data.get("highfocus_wrong", {"q1": [], "q2": [], "q3": []})
    
    is_correct = (answer == "📚 Когда нужно включить голову, сосредоточиться и работать внимательно")
    
    if is_correct:
        answers["highfocus_q3"] = {"text": answer, "is_correct": True}
        
        answers["highfocus_attempts"] = {
            "q1": {"wrong_answers": highfocus_wrong.get("q1", []), "attempts": len(highfocus_wrong.get("q1", [])) + 1},
            "q2": {"wrong_answers": highfocus_wrong.get("q2", []), "attempts": len(highfocus_wrong.get("q2", [])) + 1},
            "q3": {"wrong_answers": highfocus_wrong.get("q3", []), "attempts": len(highfocus_wrong.get("q3", [])) + 1}
        }
        
        await message.answer(HIGHFOCUS_CORRECT_Q3)
        await asyncio.sleep(1.5)
        
        quiz_result = data.get("quiz_result")
        
        try:
            await db.save_quiz_result(
                user_id=message.from_user.id,
                focus_type=quiz_result,
                answers=answers
            )
            logger.info(f"Сохранено полное прохождение квиза для user {message.from_user.id}")
        except Exception as e:
            logger.error(f"Ошибка сохранения в БД для user {message.from_user.id}: {e}", exc_info=True)
        
        await state.update_data(answers=answers)
        
        # Удаляем reply keyboard
        await message.answer("✅", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.5)
        
        # Показываем сообщение о подписке с кнопками
        await message.answer(SUBSCRIPTION_TEXT, reply_markup=get_final_keyboard())
    else:
        highfocus_wrong["q3"].append(answer)
        await state.update_data(highfocus_wrong=highfocus_wrong)
        
        error_msg = HIGHFOCUS_WRONG_Q3.get(answer, "❌ Попробуем ещё раз 👇")
        await message.answer(error_msg)
        await asyncio.sleep(1.5)
        await message.answer(HIGHFOCUS_Q3, reply_markup=get_highfocus_q3_keyboard())


# Обработчик кнопки "Уже подписан"
@dp.callback_query(F.data == "already_subscribed")
async def already_subscribed(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quiz_result = data.get("quiz_result")
    
    if quiz_result:
        # 1. Отправляем картинку с типом фокуса
        focus_image = FOCUS_TYPE_IMAGES.get(quiz_result)
        result_text = RESULTS[quiz_result]
        
        if focus_image and os.path.exists(focus_image):
            try:
                await callback.message.answer_photo(
                    photo=FSInputFile(focus_image),
                    caption=result_text
                )
            except Exception as e:
                logger.error(f"Ошибка отправки картинки типа фокуса: {e}")
                await callback.message.answer(result_text)
        else:
            await callback.message.answer(result_text)
        
        # 2. Ждём 1 секунду и отправляем картинку с рекомендуемым вкусом
        await asyncio.sleep(1)
        
        flavor_image = FLAVOR_IMAGES.get(quiz_result)
        if flavor_image and os.path.exists(flavor_image):
            try:
                await callback.message.answer_photo(photo=FSInputFile(flavor_image))
            except Exception as e:
                logger.error(f"Ошибка отправки картинки вкуса: {e}")
        
        # 3. Выдаём промокод
        await asyncio.sleep(1)
        
        promo_code = await db.assign_promo_code_to_user(callback.from_user.id)
        
        if promo_code:
            promo_message = PROMO_MESSAGE_TEMPLATE.format(promo_code=promo_code)
            await callback.message.answer(promo_message)
        else:
            await callback.message.answer(PROMO_EXHAUSTED_MESSAGE)
    
    await callback.answer("Спасибо! 🎉")
    await state.clear()


# Служебная команда для получения Telegram ID
@dp.message(Command("whoami"))
async def whoami(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


# Админ-команда: статистика промокодов
@dp.message(Command("promo_stats"))
async def promo_stats_cmd(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("⛔️ Команда доступна только администраторам.")
        return
    
    stats = await db.get_promo_stats()
    await message.answer(
        f"📊 Статистика промокодов:\n\n"
        f"Всего: {stats['total']}\n"
        f"Использовано: {stats['used']}\n"
        f"Доступно: {stats['available']}"
    )


# Админ-команда: перезапуск сервиса
@dp.message(Command(commands=["redeploy", "restart"]))
async def admin_redeploy(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("⛔️ Команда доступна только администраторам. Настрой ADMIN_IDS в переменных окружения.")
        return
    await message.answer("♻️ Перезапускаю сервис... Бот будет недоступен 3-5 секунд.")

    async def _exit_later():
        await asyncio.sleep(1)
        _os._exit(1)

    asyncio.create_task(_exit_later())


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Доступные команды:\n/start — начать\n/whoami — ваш Telegram ID\n/redeploy — перезапуск (только для админов)")


@dp.message(F.text.regexp(r"^/"))
async def unknown_command(message: Message):
    await message.answer("Команда не найдена. Попробуйте /help")


async def main():
    try:
        # Инициализация БД
        await db.init_db()
        logger.info("База данных PostgreSQL инициализирована")
        
        # Загрузка промокодов
        await load_promo_codes()
        
        # Запуск бота
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
