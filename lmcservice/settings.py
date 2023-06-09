"""
Django settings for lmcservice project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys
import platform
import subprocess

from pathlib import Path
from django.contrib.messages import constants as messages

import dj_database_url
import environ
import pdfkit

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#xmmt*)#ub)_odxh(h)+k5yb*z!3f6yufhu!mfan^%b*(jn7_$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(env('DEBUG')))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'djmoney',
    'crispy_forms',
    'django_countries',
    'crispy_bootstrap4',
    'django_json_widget',
    'django_filters',
    'djcelery_email',
    'rest_framework',
    'rest_framework.authtoken',

    'core',
    'service',
    'wallet'
]

if DEBUG: INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    # 'django.middleware.cache.FetchFromCacheMiddleware'
]

if DEBUG: MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = 'lmcservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lmcservice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(env="DO_DATABASE_URL", conn_max_age=600, conn_health_checks=True, )
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-cd'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

AWS_DEFAULT_ACL = 'public-read'
AWS_S3_REGION = env("AWS_S3_REGION")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# static settings
AWS_LOCATION = ''
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# public media settings
PUBLIC_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'lmcservice.storage.PublicMediaStorage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Bootstrap
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Authentication
AUTH_USER_MODEL = 'core.User'

LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"
LOGIN_REDIRECT_URL = "core:home"

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# DEBUG TOOLBAR
HOSTNAME = env.get_value("HOSTNAME", default="localhost:8000")

if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.get_value("REDIS_URL", default='redis://127.0.0.1:6379'),
    }
}

# CSRF_TRUSTED_ORIGINS = ["https://c855-2c0f-e00-607-a300-31f9-b0c8-8e6c-4ad9.eu.ngrok.io"]

# CELERY related settings
if DEBUG:
    CELERY_BROKER_URL = "redis://127.0.0.1:6379"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
else:
    CELERY_BROKER_URL = env('REDIS_URL')
    CELERY_RESULT_BACKEND = env('REDIS_URL')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

    # DEFAULT EMAIL
    DEFAULT_FROM_EMAIL = "noreply@lmc-rdc.com"
    ADMIN_EMAIL = "christian@tabaro.me"

# Minifying
if not DEBUG:
    HTML_MINIFY = True
    KEEP_COMMENTS_ON_MINIFYING = True
    COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')

# Security
if not DEBUG:
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    X_FRAME_OPTIONS = 'DENY'

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary debug',
    messages.INFO: 'info info',
    messages.SUCCESS: 'success success',
    messages.WARNING: 'warning warning',
    messages.ERROR: 'danger error'
}
