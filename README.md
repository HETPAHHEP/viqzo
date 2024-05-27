# Viqzo

### Описание

Проект **_Viqzo_** представляет сервис коротких ссылок.

Пользователи могут создавать обычные и кастомные ссылки, объединять их в группы, отключать при необходимости
и многое другое.

---
**⚠ {IN DEV} Проект пока находится в разработке**

### 🔍 Технические особенности

* Взаимодейтсвовать с сервисом могут анонимные (с ограничениями) и зарегистрированные пользователи.
* Для аутентификации используется JWT.
* Есть фильтрация по критериям и поиск


_Ожидает добавление:_
* _Вход по OAuth через сторонний сервис_
* _Добавление Celery для запланировнных задач_
* _Добавление кампаний_
* _и другое_



### 👨‍💻 Использованные технологии

[![Python][Python-badge]][Python-url]
[![Django REST][DRF-badge]][DRF-url]
[![PostgreSQL][Postgres-badge]][Postgres-url]

## ⚙ Начало Работы

Чтобы запустить копию проекта, следуйте инструкциям ниже.


## Запуск проекта в dev-режиме


**Необходимо создать виртуальное окружение и активировать его**

```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```

**Установить необходимые зависимости**

```bash
cd wisejournal_api
```

```bash
poetry install --with dev
```


**Зафиксировать миграции**

```bash
./manage.py migrate
```

**Создать суперпользователя и запустить проект**

```bash
./manage.py createsuperuser
```

```bash
./manage.py runserver
```
---


### 📖 API (Docs: [OpenAPI](backend/schema.yml))


---

<h5 align="center">
Автор проекта: <a href="https://github.com/HETPAHHEP">HETPAHHEP</a>
</h5>

<!-- MARKDOWN BADGES & URLs -->
[Python-badge]: https://img.shields.io/badge/Python-4db8ff?style=for-the-badge&logo=python&logoColor=%23ffeb3b

[Python-url]: https://www.python.org/

[Gunicorn-badge]: https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white

[Gunicorn-url]: https://gunicorn.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[Postgres-url]: https://www.postgresql.org/

[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Nginx-badge]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white

[Nginx-url]: https://nginx.org

[DRF-badge]: https://img.shields.io/badge/Django_REST-f44336?style=for-the-badge&logo=django

[DRF-url]: https://www.django-rest-framework.org

[Yandex-Cloud-badge]: https://img.shields.io/badge/Yandex_Cloud-white?style=for-the-badge

[Yandex-Cloud-url]: https://cloud.yandex.ru

[Github-Actions-badge]: https://img.shields.io/badge/Github_Actions-%239c27b0?style=for-the-badge&logo=github%20actions&logoColor=white

[Github-Actions-url]: https://github.com/features/actions
