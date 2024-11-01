# dev-settings.py

import os
from pathlib import Path

from dotenv import load_dotenv

from .settings import *  # noqa


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# EMAIL BACKEND FOR LOCAL DEVELOPMENT
EMAIL_HOST_USER = os.getenv("EMAIL")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "api" / "sent_emails"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # 'rest_framework_simplejwt',
    "djoser",
    "django_filters",
    "drf_spectacular",  # OpenAPI docs
    "api",
    "links",
]


# # LOGGING CONFIG
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} "
#             "{process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "telegram_message": {
#             "format": "❌ Пришла ошибка с сервера! \n\n"
#             "{levelname} {asctime} {module} "
#             "{process:d} {thread:d} {message} \n\n",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "telegram_bot": {
#             "level": "ERROR",
#             "class": "viqzo.handlers.TelegramBotHandler",
#             "chat_id": str(os.getenv("TELEGRAM_CHAT_ID")),
#             "token": str(os.getenv("TELEGRAM_BOT_TOKEN")),
#             "formatter": "telegram_message",
#         },
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': Path.joinpath(BASE_DIR, 'logs/django_error.log'),
#             'formatter': 'verbose',
#         },
#     },
#     "loggers": {
#         "django.request": {
#             "handlers": ["telegram_bot", "file"],
#             "level": "ERROR",
#         },
#     },
# }


REST_FRAMEWORK.update(  # noqa: F405
    {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
)


# SIMPLE JWT DEV-SETTINGS. FOR DEV ONLY

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=100),  # noqa: F405
    "AUTH_HEADER_TYPES": ("Bearer",),
    "SIGNING_KEY": os.getenv("DJANGO_SECRET_KEY"),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Viqzo API",
    "DESCRIPTION": "Сервис сокращенных ссылок",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
