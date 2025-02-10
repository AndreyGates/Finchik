"""Utility functions for formatting, validation, logging and other helper operations."""

from typing import Dict

def format_portfolio(portfolio: Dict[str, float]) -> str:
    """ Форматирует портфель в удобочитаемый текст. """
    return "\n".join([f"{asset}: {percentage}%" for asset, percentage in portfolio.items()])

def validate_risk_input(user_input: str) -> bool:
    """ Проверяет, является ли ввод пользователя допустимым ответом на вопросы риск-профиля. """
    return user_input in ["1", "2", "3"]

def parse_risk_score(score: int) -> str:
    """ Определяет уровень риск-профиля на основе набранных баллов. """
    if score <= 7:
        return "Консервативный"
    elif score <= 11:
        return "Умеренный"
    else:
        return "Агрессивный"

def log_action(action: str, user_id: int) -> None:
    """ Логирует действие пользователя. """
    with open("bot.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"User {user_id}: {action}\n")
