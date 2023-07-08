# Movies: Django админка для кинотеатра

Для запуска потребуется два файла с переменными окружения:

- `.env` с настройками Django + uWSGI:
```bash
cp .env.example .env
```

- `.env.db` с настройками Postgresql:
```bash
cp .env.db.example .env.db
```

Сбор статики и миграции выполняются при старте:
```bash
docker-compose up -d --build
```

После запуска, админка доступна по адресу: http://localhost/admin/

Если потребуется пользователь, то его можно создать после запуска:
```bash
docker-compose exec service python manage.py createsuperuser
```
