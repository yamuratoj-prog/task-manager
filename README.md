# Task Manager API

Простой REST API для управления задачами. Построен на **FastAPI** + **SQLAlchemy** + **SQLite**.

## Возможности

- Создание, просмотр, редактирование и удаление задач (CRUD)
- Фильтрация по статусу выполнения, пагинация
- Валидация данных (Pydantic)
- Автоматическая документация Swagger UI
- Тесты на pytest

## Структура проекта

```
task-manager-api/
├── app/
│   ├── main.py          # точка входа, создание приложения
│   ├── database.py      # подключение к БД
│   ├── models.py        # модели SQLAlchemy (таблицы)
│   ├── schemas.py       # схемы Pydantic (вход/выход API)
│   ├── crud.py          # операции с БД
│   └── routers/
│       └── tasks.py     # эндпоинты /tasks
├── tests/
│   └── test_tasks.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Установка и запуск

```bash
# 1. Клонируем репозиторий
git clone <ссылка-на-ваш-репозиторий>
cd task-manager-api

# 2. Создаём виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Ставим зависимости
pip install -r requirements.txt

# 4. Запускаем сервер
uvicorn app.main:app --reload
```

После запуска:

- API: http://127.0.0.1:8000
- Swagger UI (интерактивная документация): http://127.0.0.1:8000/docs

## Эндпоинты

| Метод  | URL             | Описание                          |
|--------|-----------------|-----------------------------------|
| GET    | `/`             | Приветствие                       |
| GET    | `/health`       | Проверка работоспособности        |
| GET    | `/tasks`        | Список задач (`?done=true&skip=0&limit=100`) |
| POST   | `/tasks`        | Создать задачу                    |
| GET    | `/tasks/{id}`   | Получить задачу                   |
| PATCH  | `/tasks/{id}`   | Изменить задачу (частично)        |
| DELETE | `/tasks/{id}`   | Удалить задачу                    |

## Примеры

```bash
# Создать задачу
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить молоко", "description": "2 литра"}'

# Список задач
curl http://127.0.0.1:8000/tasks

# Отметить выполненной
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Удалить
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Тесты

```bash
pip install -r requirements-dev.txt
pytest
```

## Настройка

Адрес БД можно поменять через переменную окружения `DATABASE_URL`
(см. `.env.example`). По умолчанию — файл `tasks.db` в корне проекта.

## Лицензия

MIT
