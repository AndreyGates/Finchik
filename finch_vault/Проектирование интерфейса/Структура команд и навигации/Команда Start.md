**Проектирование команды `/start` для Telegram-бота «Финчик»**

## **📌 Flowchart команды `/start` 

1. **Start** → **/start команда получена**
2. **Проверить, зарегистрирован ли пользователь**
    - Если **нет**:
        - **Регистрация нового пользователя** → **Отправить приветственное сообщение**
    - Если **да**:
        - **Перейти к следующему шагу**
3. **Отправить запрос на временной горизонт инвестирования**
4. **Ожидать ответ пользователя**
5. **Получить и сохранить временной горизонт**
6. **Отправить запрос на конкретную цель в соответствии с горизонтом**
7. **Ожидать ответ пользователя**
8. **Получить и сохранить конкретную цель**
9. **Предложить пользователю пройти оценку риск-профиля с помощью команды `/risk_profile`**
10. **End**

---

## **📌 Полный код команды `/start` 

```python
from telegram import Update
from telegram.ext import CallbackContext
from typing import Optional

def is_user_registered(user_id: int) -> bool:
    """ Проверяет, зарегистрирован ли пользователь в базе данных. """
    return db.check_user_exists(user_id)

def register_user(user_id: int, user_name: str) -> None:
    """ Регистрирует нового пользователя в базе данных. """
    db.add_user(user_id, user_name)

def handle_start(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает команду /start, приветствует пользователя и запускает процесс регистрации. """
    user_id: int = update.message.chat_id
    user_name: str = update.message.from_user.first_name
    
    if not is_user_registered(user_id):
        register_user(user_id, user_name)
    
    context.bot.send_message(
        chat_id=user_id,
        text=f"Привет, {user_name}! Я твой персональный Robo-Advisor **Финчик**. "
             "Помогу создать сбалансированный инвестиционный портфель и отслеживать его состояние. Давай начнем!\n\n"
             "Для начала выбери свой временной горизонт инвестирования."
    )
    ask_investment_horizon(user_id, context)

def ask_investment_horizon(user_id: int, context: CallbackContext) -> None:
    """ Отправляет пользователю сообщение с предложением выбрать временной горизонт инвестирования. """
    context.bot.send_message(
        chat_id=user_id,
        text="Выбери свой временной горизонт:\n"
             "1. Краткосрочный (1-3 года)\n"
             "2. Среднесрочный (3-7 лет)\n"
             "3. Долгосрочный (7+ лет)"
    )

def handle_horizon_selection(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает выбор временного горизонта пользователем. """
    user_id: int = update.message.chat_id
    horizon: str = update.message.text  # Получаем текст ответа

    save_user_horizon(user_id, horizon)  # Сохраняем в базе данных
    
    # Запрашиваем конкретную цель
    ask_specific_goal(user_id, context, horizon)

def save_user_horizon(user_id: int, horizon: str) -> None:
    """ Сохраняет выбранный временной горизонт инвестирования пользователя в базе данных. """
    db.save_horizon(user_id, horizon)

def ask_specific_goal(user_id: int, context: CallbackContext, horizon: str) -> None:
    """ Отправляет пользователю сообщение с предложением выбрать конкретную цель. """
    goals = {
        "1": "1. Финансовая подушка\n2. Покупка авто\n3. Первый взнос по ипотеке",
        "2": "1. Покупка недвижимости\n2. Образование детей\n3. Замена автомобиля",
        "3": "1. Финансовая независимость\n2. Пенсионные накопления\n3. Покупка загородного дома"
    }
    context.bot.send_message(
        chat_id=user_id,
        text=f"Выбери свою цель:\n{goals.get(horizon, 'Некорректный выбор')}",
    )

def handle_goal_selection(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает выбор конкретной цели пользователем. """
    user_id: int = update.message.chat_id
    goal: str = update.message.text  # Получаем текст ответа

    save_user_goal(user_id, goal)  # Сохраняем в базе данных
    
    # Предлагаем пройти оценку риск-профиля
    context.bot.send_message(
        chat_id=user_id,
        text="Отлично! Теперь ты можешь пройти оценку риск-профиля. Просто введи команду `/risk_profile`."
    )

def save_user_goal(user_id: int, goal: str) -> None:
    """ Сохраняет выбранную цель инвестирования пользователя в базе данных. """
    db.save_goal(user_id, goal)
```
