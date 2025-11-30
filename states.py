from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    """Состояния для квиза"""
    consent = State()  # Согласие на обработку персональных данных
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    # Дополнительные вопросы о High Focus
    highfocus_q1 = State()
    highfocus_q2 = State()
    highfocus_q3 = State()

