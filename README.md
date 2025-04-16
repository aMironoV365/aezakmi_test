![CI](https://github.com/aMironoV365/forkyteh_test/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-81%25-yellowgreen.svg)

# Aezakmi Test Project

Проект сервиса уведомлений для интеграции с AI-моделями

## 🚀 Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- Redis
- Celery
- pytest

## ⚙️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/aMironoV365/forkyteh_test.git
cd forkyteh_test
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 🐳 Docker

1. если хотите развернуть через Dockerfile:
```bash
docker build -t forkyteh .
docker run -p 8000:8000 forkyteh
```

2. Откройте документацию API:
```bash
http://localhost:8000/docs
```

## 🏃 Запуск без Dockerfile

1. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

2. Откройте документацию API:
```bash
http://127.0.0.1:8000/docs
```

## 📊 API Endpoints

- POST /wallet - Получить информацию о кошельке

- GET /wallets - Получить историю запросов

## 🧪 Тестирование

1. Для запуска тестов:
```bash
pytest
```

Тесты включают:

- Тестирование эндпоинтов API

- Проверку работы с базой данных

- Мокирование Tron клиента