from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    """Состояния для квиза"""
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()

