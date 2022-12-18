# Проектное задание: Docker-compose

Для запуска потребуется два файла с переменными окружения:

- `.env` с настройками Django + uWSGI:
```bash
cp .env.example .env
```

- `.env.db` с настройками Postgresql:
```bash
cp .env.db.example .env.db
```

Сбор статики и миграции выполняются при старте контейнера:
```bash
docker-compose up -d --build
```

Если потребуется пользователь, то его можно создать после запуска:
```bash
docker-compose exec service python manage.py createsuperuser
```
