Telegram LLM Support Assistant
Описание проекта
Проект представляет собой систему поддержки пользователей в Telegram с использованием LLM (TinyLlama) для генерации ответов. Состоит из четырех сервисов:

Telegram-бот: Принимает сообщения пользователей и отправляет одобренные ответы.
Веб-интерфейс (FastAPI + Vue 3): Отображает новые сообщения, позволяет генерировать и модерировать ответы.
LLM-сервис: Генерирует ответы через Ollama.
База данных: SQLite с SQLAlchemy и миграциями Alembic.

Архитектура

Разделение сервисов: Каждый сервис в отдельном контейнере (Docker Compose).
Коммуникация:
Telegram-бот сохраняет сообщения в messages (status: new, owner: user).
Веб-интерфейс запрашивает сообщения через FastAPI и отправляет в LLM-сервис.
Оператор модерирует ответы (status: pending -> answered/rejected).
Бот отправляет ответы (status: answered) пользователям.


LLM: Промпт: Ответь на сообщение пользователя: {text}.
База данных:
users: Хранит данные пользователей (включая неиспользуемые token, token_ttl).
chats: Хранит чаты.
messages: Хранит сообщения и ответы (с parent_id для возможных цепочек).



Ограничения и улучшения

Ограничения: Нет авторизации, обновление через опрос (5 сек).
Улучшения: WebSocket, JWT-авторизация, Celery для асинхронных задач.

Требования

Docker и Docker Compose
Python 3.9+
Node.js (v18+)
Ollama

Установка и запуск

Клонируйте репозиторий:
git clone <repository_url>
cd telegram-llm-support


Установите Ollama:

Инструкции
Установите TinyLlama:ollama pull tinyllama




Настройте Telegram-бот:

Получите токен через @BotFather.
Замените YOUR_TELEGRAM_BOT_TOKEN в telegram_bot/bot.py и docker-compose.yml.


Инициализируйте базу данных:
cd database
pip install alembic
alembic upgrade head


Установите зависимости фронтенда:
cd web_interface/frontend
npm install


Запустите проект:
docker-compose up --build


Доступ:

Веб-интерфейс: http://localhost:5173
FastAPI: http://localhost:8000/docs
Telegram-бот: через Telegram.



Тестирование

Отправьте сообщение боту.
Проверьте сообщения в веб-интерфейсе.
Сгенерируйте, отредактируйте или примите ответ.
Убедитесь, что ответ отправлен в Telegram.
