from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import random


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Стартовая клавиатура"""
    keyboard = [
        [InlineKeyboardButton(text="🔥 Погнали", callback_data="start_quiz")],
        [InlineKeyboardButton(text="🤔 Что за High Focus?", callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_to_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата к старту"""
    keyboard = [
        [InlineKeyboardButton(text="🔥 Погнали", callback_data="start_quiz")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_consent_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура согласия на обработку персональных данных"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Согласен", callback_data="consent_agree")],
        [InlineKeyboardButton(text="❌ Не согласен", callback_data="consent_disagree")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_1_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 1: Как вы реагируете на срочный дедлайн?"""
    options = [
        "📋 Быстро составляю чёткий план и следую ему шаг за шагом",
        "⚡️ Чувствую прилив драйва и азарта, но действую хаотично",
        "😨 Тревожусь, прокручиваю в голове негативные сценарии",
        "😔 Чувствую упадок сил, переживаю, что не справлюсь, прокрастинирую",
        "🧘‍♂️ Спокойно оцениваю объём, распределяю силы и приступаю"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_2_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 2: Что помогает вам включиться в сложную задачу?"""
    options = [
        "📊 Чёткая структура, контрольный список и видение результата",
        "🎯 Новизна, вызов, ощущение игры или соревнования",
        "🛡️ Уверенность, что риски учтены, и есть запасной план",
        "💡 Вдохновение, личная значимость и поддержка",
        "⚖️ Интерес к задаче и понимание её практической пользы"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_3_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 3: Как вы чувствуете приближение выгорания?"""
    options = [
        "😤 Всё начинает раздражать, особенно неожиданности, даже если они приятные",
        "🌀 Теряется интерес, настойчивое желание всё изменить",
        "🚨 Не могу отключить навязчивые негативные тревожные мысли",
        "🌫 Появляются пустота, апатия, всё теряет смысл",
        "🪫 Постоянная усталость, которая не проходит даже после отдыха"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_4_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 4: Что вас истощает сильнее всего в долгом проекте?"""
    options = [
        "🌪 Хаос, постоянные изменения в требованиях и отсутствие порядка",
        "🐌 Монотонность, рутина, отсутствие побед и вызовов",
        "🎲 Неопределённость результата, высокие риски и отсутствие контроля над ситуацией",
        "🔁 Механическая работа без личной вовлечённости и творчества",
        "⏳ Невозможность качественно восстанавливаться из-за плотного графика"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_5_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 5: Как вы восстанавливаетесь после стресса?"""
    options = [
        "🧹 Навожу порядок в пространстве, составляю планы на будущее",
        "🎪 Пробую что-то новое: место, хобби, активность. Ищу адреналин",
        "🛌 Ухожу в тихую, спокойную рутину, минимизирую контакты",
        "🎨 Уединяюсь, слушаю музыку, погружаюсь в творчество или природу",
        "🍃 Сон, хобби, общение, спорт — всё понемногу"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_highfocus_q1_keyboard() -> ReplyKeyboardMarkup:
    """High Focus Вопрос 1: High Focus — это…"""
    options = [
        "🥤 Новый энергетик на основе молока «ЭкоНива»",
        "🧠 Молочный напиток для концентрации и энергии на основе гуараны и L-теанина",
        "☕️ Кофейный напиток для бодрости и энергии"
    ]
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_highfocus_q2_keyboard() -> ReplyKeyboardMarkup:
    """High Focus Вопрос 2: Зачем пить High Focus?"""
    options = [
        "😵 Чтобы взбодриться и «включить турборежим»",
        "🚀 Чтобы резко поднять энергию, как у энергетиков",
        "🧠 Чтобы поддерживать концентрацию, ясность и мягкий уровень энергии в течение дня"
    ]
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_highfocus_q3_keyboard() -> ReplyKeyboardMarkup:
    """High Focus Вопрос 3: В какой ситуации High Focus подходит лучше всего?"""
    options = [
        "😵 Когда нужно бодрствовать всю ночь",
        "🍔 Когда хочешь заменить приём пищи",
        "📚 Когда нужно включить голову, сосредоточиться и работать внимательно"
    ]
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_final_keyboard() -> InlineKeyboardMarkup:
    """Финальная клавиатура с подпиской"""
    keyboard = [
        [InlineKeyboardButton(text="🔗 Подписаться", url="https://t.me/high_focusEN")],
        [InlineKeyboardButton(text="✅ Уже подписан", callback_data="already_subscribed")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
