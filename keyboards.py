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
        "🔒 Быстро собираюсь, делаю план и иду по нему",
        "😰 Начинаю тревожиться и прокручивать негативные сценарии",
        "😔 Чувствую упадок и прокрастинирую",
        "🌋 Заряжаюсь энергией, но могу вспылить",
        "⚡ Бросаюсь в задачу с азартом, но хаотично",
        "🎭 То включаюсь, то выгораю — скачки энергии",
        "☯ Спокойно адаптируюсь, распределяю силы"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_2_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 2: Что помогает вам включиться в сложную задачу?"""
    options = [
        "🔒 План и контроль",
        "😰 Уверенность, что всё под контролем",
        "😔 Поддержка и признание",
        "🌋 Азарт и драйв",
        "⚡ Новизна и вызов",
        "🎭 Вдохновение и увлечённость",
        "☯ Баланс интереса и пользы"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_3_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 3: Как вы чувствуете приближение выгорания?"""
    options = [
        "🔒 Всё раздражает, если что-то идёт не по плану",
        "😰 Не могу отключить тревожные мысли",
        "😔 Пустота и апатия",
        "🌋 Вспышки гнева по мелочам",
        "⚡ Теряю интерес, ищу острые ощущения",
        "🎭 Настроение скачет",
        "☯ Постоянная усталость, даже после отдыха"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_4_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 4: Что вас больше всего истощает в долгом проекте?"""
    options = [
        "🔒 Хаос и постоянные изменения",
        "😰 Неопределенность и риски",
        "😔 Рутина и отсутствие смысла",
        "🌋 Необходимость сдерживать эмоции",
        "⚡ Монотонность без быстрых побед",
        "🎭 Конфликты и негативная атмосфера",
        "☯ Нет времени на восстановление"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_5_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 5: Как вы восстанавливаетесь после стресса?"""
    options = [
        "🔒 Навожу порядок, планирую",
        "😰 Ухожу в спокойную рутину",
        "😔 Уединяюсь в тишине",
        "🌋 Выплескиваю эмоции через спорт или музыку",
        "⚡ Меняю обстановку, ищу новое",
        "🎭 Провожу время с близкими",
        "☯ Сон, еда, хобби, баланс"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_highfocus_q1_keyboard() -> ReplyKeyboardMarkup:
    """High Focus Вопрос 1: High Focus — это…"""
    options = [
        "🥤 Новый энергетик на основе молока Эконива",
        "🧠 Молочный напиток для концентрации и энергии на основе гуараны и L-теанина",
        "☕️ Кофейный напиток для бодрости и энергии"
    ]
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_highfocus_q2_keyboard() -> ReplyKeyboardMarkup:
    """High Focus Вопрос 2: Зачем вообще пить High Focus?"""
    options = [
        "😵 Чтобы взбодриться и «врубить турбо-режим»",
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

