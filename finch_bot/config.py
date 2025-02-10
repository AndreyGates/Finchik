"""Configuration module for loading and managing environment variables and application settings."""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# API-ключ для MOEX
MOEX_API_KEY = os.getenv("MOEX_API_KEY")

# Путь к базе данных
DB_PATH = os.getenv("DB_PATH", "database/finch.db")

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# Настройки обновления портфеля
AUTO_REBALANCE = os.getenv("AUTO_REBALANCE", "True").lower() == "true"
UPDATE_FREQUENCY = os.getenv(
    "UPDATE_FREQUENCY", 
    "quarterly"
)  # monthly, quarterly, yearly

# Настройки API MOEX
MOEX_INDEX_API = "https://iss.moex.com/iss/engines/stock/markets/index/indices/{}/values.json"

# Проверяем, загружены ли основные переменные
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")
