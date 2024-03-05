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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# EMAIL BACKEND FOR LOCAL DEVELOPMENT
EMAIL_HOST_USER = os.getenv('EMAIL')

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'api' / 'sent_emails'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',

    'drf_spectacular',  # OpenAPI docs

    'api',
    'links',
]

REST_FRAMEWORK.update(
    {'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'}
)


SPECTACULAR_SETTINGS = {
    'TITLE': 'Viqzo API',
    'DESCRIPTION': 'Сервис сокращенный ссылок',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
