"""Module for handling the /start command and initial user registration flow."""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)
from telegram.constants import ParseMode

from database.db_handler import DB as db

# Define states
HORIZON, GOAL = range(2)

def is_user_registered(user_id: int) -> bool:
    """ Проверяет, зарегистрирован ли пользователь в базе данных. """
    return db.check_user_exists(user_id)

def register_user(user_id: int, user_name: str) -> None:
    """ Регистрирует нового пользователя в базе данных. """
    db.add_user(user_id, user_name)

async def start(update: Update, _: CallbackContext) -> int:
    """Обработчик команды /start, приветствует пользователя и запускает процесс регистрации."""
    user_id: int = update.message.chat_id
    user_name: str = update.message.from_user.first_name

    if not is_user_registered(user_id):
        register_user(user_id, user_name)

    keyboard = [
        [InlineKeyboardButton("Краткосрочный (1-3 года)", callback_data='horizon_1')],
        [InlineKeyboardButton("Среднесрочный (3-7 лет)", callback_data='horizon_2')],
        [InlineKeyboardButton("Долгосрочный (7+ лет)", callback_data='horizon_3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Привет, {user_name}! Я твой персональный Robo-Advisor <b>Финчик</b>.\n\n"
             "💼 Помогу создать сбалансированный инвестиционный портфель и отслеживать его состояние. Давай начнем!\n\n"
             "⏳ Для начала выбери свой временной горизонт инвестирования:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return HORIZON

async def handle_horizon_selection(update: Update, _: CallbackContext) -> int:
    """Обрабатывает выбор временного горизонта инвестирования пользователем."""
    query = update.callback_query
    await query.answer()

    user_id: int = query.message.chat_id
    horizon: str = query.data.split('_')[1]  # Extract number from 'horizon_X'

    save_user_horizon(user_id, horizon)

    goals_keyboard = []
    if horizon == '1':
        goals_keyboard = [
            [InlineKeyboardButton("Финансовая подушка", callback_data='goal_1')],
            [InlineKeyboardButton("Покупка авто", callback_data='goal_2')],
            [InlineKeyboardButton("Первый взнос по ипотеке", callback_data='goal_3')]
        ]
    elif horizon == '2':
        goals_keyboard = [
            [InlineKeyboardButton("Покупка недвижимости", callback_data='goal_1')],
            [InlineKeyboardButton("Образование детей", callback_data='goal_2')],
            [InlineKeyboardButton("Замена автомобиля", callback_data='goal_3')]
        ]
    else:
        goals_keyboard = [
            [InlineKeyboardButton("Финансовая независимость", callback_data='goal_1')],
            [InlineKeyboardButton("Пенсионные накопления", callback_data='goal_2')],
            [InlineKeyboardButton("Покупка загородного дома", callback_data='goal_3')]
        ]

    reply_markup = InlineKeyboardMarkup(goals_keyboard)
    await query.edit_message_text(
        text="✅ Отлично! Теперь выбери свою цель:",
        reply_markup=reply_markup
    )
    return GOAL

async def handle_goal_selection(update: Update, _: CallbackContext) -> int:
    """Обрабатывает выбор инвестиционной цели пользователем."""
    query = update.callback_query
    await query.answer()

    user_id: int = query.message.chat_id
    goal: str = query.data.split('_')[1]  # Extract number from 'goal_X'

    save_user_goal(user_id, goal)

    await query.edit_message_text(
        text="🎯 Отлично! Теперь ты можешь пройти оценку риск-профиля. Просто введи команду /risk_profile"
    )
    return ConversationHandler.END

def save_user_horizon(user_id: int, horizon: str) -> None:
    """ Сохраняет выбранный временной горизонт инвестирования пользователя в базе данных. """
    db.save_horizon(user_id, horizon)

def save_user_goal(user_id: int, goal: str) -> None:
    """ Сохраняет выбранную цель инвестирования пользователя в базе данных. """
    db.save_goal(user_id, goal)

# Create conversation handler
start_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        HORIZON: [CallbackQueryHandler(handle_horizon_selection, pattern='^horizon_')],
        GOAL: [CallbackQueryHandler(handle_goal_selection, pattern='^goal_')]
    },
    fallbacks=[]
)

__all__ = ['start_conversation']
