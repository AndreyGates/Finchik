"""Database handler module for SQLite operations and user data management."""

import sqlite3
from typing import Optional
from config import DB_PATH

class DatabaseHandler:
    """Класс для управления базой данных SQLite"""
    def __init__(self, db_path: str = DB_PATH):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Создает таблицы в базе данных, если они не существуют"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                horizon TEXT,
                goal TEXT,
                risk_profile TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolios (
                user_id INTEGER PRIMARY KEY,
                portfolio TEXT,
                expected_return REAL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.connection.commit()

    def add_user(self, user_id: int, user_name: str) -> None:
        """Добавляет нового пользователя в базу данных"""
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, name) 
            VALUES (?, ?)
        ''', (user_id, user_name))
        self.connection.commit()

    def save_goal(self, user_id: int, goal: str) -> None:
        """Сохраняет цель пользователя"""
        self.cursor.execute("UPDATE users SET goal = ? WHERE user_id = ?", (goal, user_id))
        self.connection.commit()

    def save_risk_profile(self, user_id: int, risk_profile: str) -> None:
        """Сохраняет риск-профиль пользователя"""
        self.cursor.execute("UPDATE users SET risk_profile = ? WHERE user_id = ?", (risk_profile, user_id))
        self.connection.commit()

    def get_user_goal(self, user_id: int) -> Optional[str]:
        """Возвращает цель пользователя"""
        self.cursor.execute("SELECT goal FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_risk_profile(self, user_id: int) -> Optional[str]:
        """Возвращает риск-профиль пользователя"""
        self.cursor.execute("SELECT risk_profile FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_portfolio(self, user_id: int, portfolio: str, expected_return: float) -> None:
        """Сохраняет портфель пользователя"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO portfolios (user_id, portfolio, expected_return) VALUES (?, ?, ?)",
            (user_id, portfolio, expected_return)
        )
        self.connection.commit()

    def get_portfolio(self, user_id: int) -> Optional[str]:
        """Возвращает портфель пользователя"""
        self.cursor.execute("SELECT portfolio FROM portfolios WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self) -> None:
        """Закрывает соединение с базой данных"""
        self.connection.close()

    def check_user_exists(self, user_id: int) -> bool:
        """Проверяет существование пользователя в базе данных."""
        self.cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        return bool(self.cursor.fetchone())

    def save_horizon(self, user_id: int, horizon: str) -> None:
        """Сохраняет временной горизонт инвестирования пользователя"""
        self.cursor.execute("UPDATE users SET horizon = ? WHERE user_id = ?", (horizon, user_id))
        self.connection.commit()

# Создаем экземпляр базы данных
DB = DatabaseHandler()
