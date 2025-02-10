**Проектирование команды `/risk_profile` для Telegram-бота «Финчик»**

## **📌 Flowchart команды `/risk_profile`**

1. **Start** → **/risk_profile команда получена**
2. **Отправить пользователю приветствие и объяснить процесс оценки риск-профиля**
3. **Задать вопросы по оценке риск-профиля** (поочередно, с вариантами ответов):
    - Вопрос 1: "Как ты относишься к убыткам?"
    - Вопрос 2: "Какой у тебя инвестиционный горизонт?"
    - Вопрос 3: "Что для тебя важнее: стабильность или высокая доходность?"
    - Вопрос 4: "Какую просадку портфеля ты готов терпеть?"
4. **Ожидать ответов пользователя на каждый вопрос**
5. **Рассчитать общий риск-профиль на основе ответов** (консервативный, умеренный, агрессивный)
6. **Сохранить результат в базе данных**
7. **Отправить пользователю результат и рекомендации по инвестициям**
8. **End**

---

## **📌 Полный код команды `/risk_profile

```python
from telegram import Update
from telegram.ext import CallbackContext
from typing import Dict

# Словарь для хранения ответов пользователей
user_responses: Dict[int, Dict[str, int]] = {}

# Вопросы для оценки риск-профиля
risk_questions = [
    "Как ты относишься к убыткам?\n"
    "1. Не готов терять вообще (1 балл)\n"
    "2. Готов к небольшим просадкам (2 балла)\n"
    "3. Готов к высоким рискам ради роста (3 балла)",
    
    "Какой у тебя инвестиционный горизонт?\n"
    "1. 1-3 года (1 балл)\n"
    "2. 3-7 лет (2 балла)\n"
    "3. 7+ лет (3 балла)",
    
    "Что для тебя важнее: стабильность или высокая доходность?\n"
    "1. Стабильность (1 балл)\n"
    "2. Баланс между доходностью и риском (2 балла)\n"
    "3. Максимальный рост (3 балла)",
    
    "Какую просадку портфеля ты готов терпеть?\n"
    "1. До -5% (1 балл)\n"
    "2. До -15% (2 балла)\n"
    "3. До -30% и выше (3 балла)"
]

# Обработка команды /risk_profile
def handle_risk_profile(update: Update, context: CallbackContext) -> None:
    """ Запускает процесс оценки риск-профиля. """
    user_id: int = update.message.chat_id
    user_responses[user_id] = {"score": 0, "question_index": 0}
    
    context.bot.send_message(
        chat_id=user_id,
        text="Давай определим твой риск-профиль. Я задам тебе 4 вопроса. Выбирай номер ответа."
    )
    ask_next_question(user_id, context)

# Функция отправки следующего вопроса
def ask_next_question(user_id: int, context: CallbackContext) -> None:
    """ Отправляет пользователю следующий вопрос из списка. """
    user_data = user_responses.get(user_id)
    
    if user_data and user_data["question_index"] < len(risk_questions):
        context.bot.send_message(
            chat_id=user_id,
            text=risk_questions[user_data["question_index"]]
        )
    else:
        calculate_risk_profile(user_id, context)

# Обработчик ответов на вопросы
def handle_risk_response(update: Update, context: CallbackContext) -> None:
    """ Обрабатывает ответ пользователя и переходит к следующему вопросу. """
    user_id: int = update.message.chat_id
    user_data = user_responses.get(user_id)
    
    if user_data is None or user_data["question_index"] >= len(risk_questions):
        return
    
    answer = update.message.text.strip()
    if answer in ["1", "2", "3"]:
        user_data["score"] += int(answer)
        user_data["question_index"] += 1
        ask_next_question(user_id, context)
    else:
        context.bot.send_message(chat_id=user_id, text="Пожалуйста, выбери 1, 2 или 3.")

# Функция расчета итогового риск-профиля
def calculate_risk_profile(user_id: int, context: CallbackContext) -> None:
    """ Рассчитывает риск-профиль на основе набранных баллов и отправляет результат. """
    user_data = user_responses.get(user_id)
    if user_data is None:
        return
    
    score = user_data["score"]
    
    if score <= 7:
        profile = "🔵 Консервативный"
    elif score <= 11:
        profile = "🟠 Умеренный"
    else:
        profile = "🔴 Агрессивный"
    
    db.save_risk_profile(user_id, profile)
    
    context.bot.send_message(
        chat_id=user_id,
        text=f"Твой риск-профиль: **{profile}**. Теперь можешь перейти к формированию портфеля!"
    )
```