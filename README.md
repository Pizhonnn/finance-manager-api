markdown
# 💰 Finance Manager API

Полноценный Fullstack-сервис для управления личными финансами. 
Позволяет создавать кошельки в разных валютах, отслеживать доходы/расходы и вести историю транзакций. 
Проект написан с упором на чистую архитектуру и современные практики разработки на Python.

## 🛠 Стек технологий

* **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (ORM), Pydantic (валидация)
* **База данных:** PostgreSQL 16, Alembic (миграции)
* **Инфраструктура:** Docker, Docker Compose
* **Тестирование и качество кода:** Pytest (интеграционные тесты), Ruff (линтер), Mypy (статическая типизация)
* **Frontend:** HTML5, TailwindCSS, Vanilla JS (раздается напрямую из FastAPI)

## 📸 Скриншот интерфейса

![Интерфейс приложения](screenshot.png)

## 🚀 Как запустить проект

Для запуска вам понадобятся только установленные **Docker** и **Docker Compose**.

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/pizhonnn/finance-manager-api.git
   cd finance-manager-api
Запустите контейнеры:

docker compose up --build

Приложение будет доступно по адресам:

Фронтенд: http://localhost:8080/

Swagger UI (Документация API): http://localhost:8080/docs

🧪 Тестирование
Проект покрыт интеграционными тестами с использованием Pytest и SQLite (in-memory). Тесты изолированы и не требуют запущенной базы данных PostgreSQL.

# Установите зависимости локально
pip install -r requirements.txt

# Запустите тесты
pytest tests/ -v
🗄 Миграции базы данных
В проекте используется Alembic для контроля версий схемы базы данных. При первом запуске таблицы создаются автоматически (в Docker), но если вы хотите применить миграции вручную:

alembic upgrade head
🏗 Архитектура проекта
Проект разделен на слои для удобства поддержки и тестирования (паттерн Service/Repository):

app/api — Роутеры (эндпоинты FastAPI)

app/service — Бизнес-логика (проверки, транзакции)

app/repository — Работа с базой данных (SQLAlchemy запросы)

app/models — ORM-модели

app/schemas — Схемы Pydantic (валидация запросов и ответов)

tests — Интеграционные тесты (Pytest)

*Автор: [pizhonnn](https://github.com/pizhonnn)*
