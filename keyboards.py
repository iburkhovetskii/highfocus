from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def get_question_1_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 1: Когда тебе нужно сосредоточиться, ты..."""
    keyboard = [
        [InlineKeyboardButton(text="💡 Ищу вдохновение и новые подходы", callback_data="q1_creative")],
        [InlineKeyboardButton(text="🧠 Раскладываю задачу по шагам", callback_data="q1_analytical")],
        [InlineKeyboardButton(text="⚡️ Просто начинаю делать — фокус приходит в действии", callback_data="q1_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_2_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 2: Что помогает тебе войти в "рабочий поток"?"""
    keyboard = [
        [InlineKeyboardButton(text="🎶 Настроение, музыка, атмосфера", callback_data="q2_creative")],
        [InlineKeyboardButton(text="📋 Чёткий план и порядок", callback_data="q2_analytical")],
        [InlineKeyboardButton(text="🚀 Азарт, дедлайн и движение", callback_data="q2_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_3_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 3: Что чаще всего мешает тебе сфокусироваться?"""
    keyboard = [
        [InlineKeyboardButton(text="💭 Однообразие, скука", callback_data="q3_creative")],
        [InlineKeyboardButton(text="📱 Шум, уведомления, отвлекающие люди", callback_data="q3_analytical")],
        [InlineKeyboardButton(text="💤 Усталость и низкий уровень энергии", callback_data="q3_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_4_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 4: Как ты обычно решаешь сложные задачи?"""
    keyboard = [
        [InlineKeyboardButton(text="💡 Ищу нестандартное решение", callback_data="q4_creative")],
        [InlineKeyboardButton(text="🧠 Разбиваю на части и иду по шагам", callback_data="q4_analytical")],
        [InlineKeyboardButton(text="⚡️ Беру и делаю — разберусь по пути", callback_data="q4_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_5_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 5: Что для тебя признак настоящего фокуса?"""
    keyboard = [
        [InlineKeyboardButton(text="💡 Поток идей и вдохновение", callback_data="q5_creative")],
        [InlineKeyboardButton(text="🧠 Чёткие мысли и контроль над процессом", callback_data="q5_analytical")],
        [InlineKeyboardButton(text="⚡️ Максимальная скорость и энергия", callback_data="q5_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_6_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 6: Когда ты чувствуешь себя продуктивнее всего?"""
    keyboard = [
        [InlineKeyboardButton(text="🌅 Утром — когда всё только начинается", callback_data="q6_analytical")],
        [InlineKeyboardButton(text="🌇 Днём — в потоке задач и общения", callback_data="q6_creative")],
        [InlineKeyboardButton(text="🌙 Вечером / ночью — когда никто не мешает", callback_data="q6_energetic")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_7_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 7: Интересна ли тебе альтернатива кофе..."""
    keyboard = [
        [InlineKeyboardButton(text="⚡️ Да, это то, чего не хватает", callback_data="q7_yes_need")],
        [InlineKeyboardButton(text="☕️ Возможно, если вкус будет приятный", callback_data="q7_maybe_taste")],
        [InlineKeyboardButton(text="🤷 Интересно попробовать", callback_data="q7_curious")],
        [InlineKeyboardButton(text="🚫 Нет, я остаюсь при кофе", callback_data="q7_no_coffee")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_8_keyboard() -> InlineKeyboardMarkup:
    """Вопрос 8: Какой вкус понравился больше всего?"""
    keyboard = [
        [InlineKeyboardButton(text="🍐 Груша–Пармезан", callback_data="q8_pear")],
        [InlineKeyboardButton(text="🍯 Солёная карамель", callback_data="q8_caramel")],
        [InlineKeyboardButton(text="🍫 Брауни", callback_data="q8_brownie")],
        [InlineKeyboardButton(text="🤔 Ещё не пробовал, но хочу", callback_data="q8_want")],
        [InlineKeyboardButton(text="🤷 Пока не решил", callback_data="q8_undecided")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_final_keyboard() -> InlineKeyboardMarkup:
    """Финальная клавиатура с подпиской"""
    keyboard = [
        [InlineKeyboardButton(text="🔗 Подписаться", url="https://t.me/high_focusEN")],
        [InlineKeyboardButton(text="✅ Уже подписан", callback_data="already_subscribed")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

