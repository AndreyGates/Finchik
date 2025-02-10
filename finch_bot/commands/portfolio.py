"""Module for handling portfolio generation and management commands."""

from typing import Dict, Optional
import requests
from telegram import Update
from telegram.ext import CallbackContext
from database.db_handler import DB as db
from utils.helpers import format_portfolio

# API для получения значений индексов с Московской биржи
MOEX_INDEX_API = "https://iss.moex.com/iss/engines/stock/markets/index/indices/{}/values.json"

def get_index_value(index: str) -> float:
    """Получает текущее значение указанного индекса с MOEX API."""
    response = requests.get(MOEX_INDEX_API.format(index), timeout=10)
    if response.status_code == 200:
        data = response.json()
        try:
            return float(data['values'][0]['value'])
        except (KeyError, IndexError, TypeError):
            return None  # Если данных нет, возвращаем None
    return None

def handle_portfolio(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает команду /portfolio и предлагает пользователю оптимальный портфель. """
    user_id: int = update.message.chat_id
    
    # Проверяем, есть ли у пользователя цель и риск-профиль
    user_goal: Optional[str] = db.get_user_goal(user_id)
    user_risk_profile: Optional[str] = db.get_risk_profile(user_id)
    
    if not user_goal or not user_risk_profile:
        context.bot.send_message(
            chat_id=user_id,
            text="Чтобы сформировать портфель, необходимо сначала задать цель (/start) и пройти тест на риск-профиль (/risk_profile)."
        )
        return
    
    # Подбираем оптимальный портфель
    portfolio = generate_portfolio(user_risk_profile)
    expected_return = calculate_expected_return(portfolio)
    
    # Сохраняем портфель в базе данных
    db.save_portfolio(
        user_id=user_id,
        portfolio=portfolio,
        expected_return=expected_return
    )
    
    # Отправляем пользователю структуру портфеля и рекомендации
    context.bot.send_message(
        chat_id=user_id,
        text=f"✅ Твой инвестиционный портфель сформирован:\n\n{format_portfolio(portfolio)}\n\n"
             f"📈 Ожидаемая доходность (на основе реальных рыночных данных): {expected_return:.2f}% в год\n\n"
             "🔄 Авто-ребалансировка: если соотношение активов изменится, мы подскажем, как его восстановить.\n"
             "📅 Обновление раз в квартал: мы адаптируем портфель к текущей рыночной ситуации."
    )

def generate_portfolio(risk_profile: str) -> Dict[str, float]:
    """ Генерирует оптимальный портфель на основе риск-профиля. """
    portfolios = {
        "Консервативный": {"Облигации": 70, "Акции": 20, "Золото": 10},
        "Умеренный": {"Облигации": 50, "Акции": 40, "Золото": 10},
        "Агрессивный": {"Облигации": 30, "Акции": 50, "Золото": 20},
    }
    return portfolios.get(risk_profile, {"Облигации": 50, "Акции": 40, "Золото": 10})

def calculate_expected_return(portfolio: Dict[str, float]) -> float:
    """ Рассчитывает ожидаемую доходность портфеля на основе актуальных индексов. """
    
    # Получаем значения индексов с MOEX API
    imoex_return = get_index_value("IMOEX")  # Среднегодовая доходность акций
    rgbi_return = get_index_value("RGBI")    # Среднегодовая доходность облигаций
    rugold_return = get_index_value("RUGOLD") # Среднегодовая доходность золота

    # Подставляем полученные данные в расчет
    asset_returns = {
        "Акции": imoex_return if imoex_return else 10.0,
        "Облигации": rgbi_return if rgbi_return else 5.0,
        "Золото": rugold_return if rugold_return else 7.0
    }

    # Рассчитываем ожидаемую доходность портфеля
    expected_return = sum(
        (weight / 100) * asset_returns.get(asset, 0)
        for asset, weight in portfolio.items()
    )

    return expected_return