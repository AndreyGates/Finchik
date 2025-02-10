"""Module for handling risk profile assessment and user risk tolerance evaluation."""

from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)
from database.db_handler import DB as db

# Состояния диалога
ANSWERING_QUESTIONS = 1

# Словарь для хранения ответов пользователей
user_responses: Dict[int, Dict[str, int]] = {}

# Вопросы и варианты ответов
risk_questions = [
    {
        "question": "❓ Как ты относишься к убыткам?",
        "options": [
            "Не готов терять вообще",
            "Готов к небольшим просадкам",
            "Готов к высоким рискам ради роста"
        ]
    },
    {
        "question": "⏳ Какой у тебя инвестиционный горизонт?",
        "options": [
            "1-3 года",
            "3-7 лет",
            "7+ лет"
        ]
    },
    {
        "question": "⚖️ Что для тебя важнее: стабильность или высокая доходность?",
        "options": [
            "Стабильность",
            "Баланс между доходностью и риском",
            "Максимальный рост"
        ]
    },
    {
        "question": "📊 Какую просадку портфеля ты готов терпеть?",
        "options": [
            "До -5%",
            "До -15%",
            "До -30% и выше"
        ]
    }
]

def get_keyboard(question_index: int) -> InlineKeyboardMarkup:
    """Создает вертикальную клавиатуру с вариантами ответов."""
    options = risk_questions[question_index]["options"]
    keyboard = [
        [InlineKeyboardButton(f"1️⃣ {options[0]}", callback_data='1')],
        [InlineKeyboardButton(f"2️⃣ {options[1]}", callback_data='2')],
        [InlineKeyboardButton(f"3️⃣ {options[2]}", callback_data='3')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def handle_risk_profile(update: Update, context: CallbackContext) -> int:
    """Запускает процесс оценки риск-профиля."""
    user_id = update.message.chat_id
    user_responses[user_id] = {"score": 0, "question_index": 0}

    await update.message.reply_text(
        "📝 Давай определим твой риск-профиль. Я задам тебе 4 вопроса. Выбирай вариант ответа."
    )
    await ask_next_question(user_id, context)
    return ANSWERING_QUESTIONS

async def ask_next_question(user_id: int, context: CallbackContext) -> None:
    """Отправляет пользователю следующий вопрос из списка."""
    user_data = user_responses.get(user_id)

    if user_data and user_data["question_index"] < len(risk_questions):
        question_index = user_data["question_index"]
        await context.bot.send_message(
            chat_id=user_id,
            text=risk_questions[question_index]["question"],
            reply_markup=get_keyboard(question_index)
        )

async def handle_risk_response(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ответ пользователя и переходит к следующему вопросу."""
    query = update.callback_query
    user_id = query.message.chat_id
    user_data = user_responses.get(user_id)

    if user_data is None or user_data["question_index"] >= len(risk_questions):
        await query.answer()
        return ConversationHandler.END

    answer = query.data
    if answer in ["1", "2", "3"]:
        user_data["score"] += int(answer)
        user_data["question_index"] += 1
        await query.answer()

        if user_data["question_index"] < len(risk_questions):
            await ask_next_question(user_id, context)
            return ANSWERING_QUESTIONS
        else:
            await calculate_risk_profile(user_id, context)
            return ConversationHandler.END
    else:
        await query.answer("Пожалуйста, выберите один из предложенных вариантов")
        return ANSWERING_QUESTIONS

async def calculate_risk_profile(user_id: int, context: CallbackContext) -> None:
    """Рассчитывает риск-профиль на основе набранных баллов и отправляет результат."""
    user_data = user_responses.get(user_id)
    if user_data is None:
        return

    score = user_data["score"]

    if score <= 7:
        profile = "🔵 Консервативный инвестор\n💼 Низкий риск, стабильный доход"
    elif score <= 11:
        profile = "🟠 Умеренный инвестор\n💼 Средний риск, сбалансированный подход"
    else:
        profile = "🔴 Агрессивный инвестор\n💼 Высокий риск, максимальный рост"

    db.save_risk_profile(user_id, profile)

    await context.bot.send_message(
        chat_id=user_id,
        text=f"🎯 Анализ завершен!\n\nТвой риск-профиль:\n{profile}\n\n✨ Теперь можешь перейти к формированию портфеля!"
    )

# Create conversation handler
risk_profile_conversation = ConversationHandler(
    entry_points=[CommandHandler('risk_profile', handle_risk_profile)],
    states={
        ANSWERING_QUESTIONS: [CallbackQueryHandler(handle_risk_response)]
    },
    fallbacks=[]
)

__all__ = ['risk_profile_conversation']
