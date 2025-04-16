# Aezakmi Test Project

Проект сервиса уведомлений для интеграции с AI-моделями

## 🚀 Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- Redis
- Celery
- pytest
- Мок для имитации внешних зависимостей в тестах.

## ⚙️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/aMironoV365/aezakmi_test.git
cd aezakmi_test
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

1. Перед запуском убедитесь, что файл .env выглядит следующим образом:
```
REDIS_URL="redis://redis:6379/0"
REDIS_BACKEND="redis://redis:6379/0"
```

2. Разворачивание проекта через Docker-compose:
```bash
docker-compose up --build
```

3. Откройте документацию API:
```bash
http://localhost:8000/docs
```



## 📊 API Endpoints

- POST /create_notification - Создание уведомления

- GET /notification_list - Получение списка уведомлений

- GET /notification{notification_id} - Получение уведомления по ID

- POST /notification{id}/mark_read - Отметить уведомление как прочитанное

## 🧪 Тестирование

1. Перед запуском тестов убедитесь что в файле .env у вас выглядит следующим образом:
```
REDIS_URL="redis://localhost:6379/0"
REDIS_BACKEND="redis://localhost:6379/0"
```

2. Для запуска тестов:
```bash
pytest
```

Тесты включают:

- Тестирование эндпоинтов API