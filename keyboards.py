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
        [InlineKeyboardButton(text="📄 Прочитать полностью", callback_data="consent_read")],
        [InlineKeyboardButton(text="❌ Не согласен", callback_data="consent_disagree")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_1_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 1: Когда тебе нужно сосредоточиться, ты..."""
    options = [
        "💡 Ищу вдохновение и новые подходы",
        "🧠 Раскладываю задачу по шагам",
        "⚡️ Просто начинаю делать — фокус приходит в действии"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_2_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 2: Что помогает тебе войти в "рабочий поток"?"""
    options = [
        "🎶 Настроение, музыка, атмосфера",
        "📋 Чёткий план и порядок",
        "🚀 Азарт, дедлайн и движение"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_3_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 3: Что чаще всего мешает тебе сфокусироваться?"""
    options = [
        "💭 Однообразие, скука",
        "📱 Шум, уведомления, отвлекающие люди",
        "💤 Усталость и низкий уровень энергии"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_4_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 4: Как ты обычно решаешь сложные задачи?"""
    options = [
        "💡 Ищу нестандартное решение",
        "🧠 Разбиваю на части и иду по шагам",
        "⚡️ Беру и делаю — разберусь по пути"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_5_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 5: Что для тебя признак настоящего фокуса?"""
    options = [
        "💡 Поток идей и вдохновение",
        "🧠 Чёткие мысли и контроль над процессом",
        "⚡️ Максимальная скорость и энергия"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_6_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 6: Когда ты чувствуешь себя продуктивнее всего?"""
    options = [
        "🌅 Утром — когда всё только начинается",
        "🌇 Днём — в потоке задач и общения",
        "🌙 Вечером / ночью — когда никто не мешает"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_7_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 7: Интересна ли тебе альтернатива кофе..."""
    options = [
        "⚡️ Да, это то, чего не хватает",
        "☕️ Возможно, если вкус будет приятный",
        "🤷 Интересно попробовать",
        "🚫 Нет, я остаюсь при кофе"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_question_8_keyboard() -> ReplyKeyboardMarkup:
    """Вопрос 8: Какой вкус понравился больше всего?"""
    options = [
        "🍐 Груша–Пармезан",
        "🍯 Солёная карамель",
        "🍫 Брауни",
        "🤔 Ещё не пробовал, но хочу",
        "🤷 Пока не решил"
    ]
    random.shuffle(options)
    keyboard = [[KeyboardButton(text=option)] for option in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_final_keyboard() -> InlineKeyboardMarkup:
    """Финальная клавиатура с подпиской"""
    keyboard = [
        [InlineKeyboardButton(text="🔗 Подписаться", url="https://t.me/high_focusEN")],
        [InlineKeyboardButton(text="✅ Уже подписан", callback_data="already_subscribed")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

