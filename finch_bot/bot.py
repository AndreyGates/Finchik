"""Telegram bot main module for investment portfolio management and risk profile assessment."""

import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CallbackContext
from config import BOT_TOKEN
from commands.start import start_conversation
from commands.risk_profile import risk_profile_conversation
from commands.portfolio import handle_portfolio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def portfolio(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /portfolio"""
    await handle_portfolio(update, context)

async def set_commands(application: Application) -> None:
    """Настраивает команды бота, которые отображаются в меню"""
    commands = [
        BotCommand("start", "🚀 Начать работу с ботом"),
        BotCommand("risk_profile", "📊 Определить профиль риска")
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    """Запускает бота и регистрирует команды"""
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(start_conversation)
    application.add_handler(risk_profile_conversation)

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
