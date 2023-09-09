"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

from celery.schedules import crontab

from datetime import datetime, timedelta
# import django_filter
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")  # ""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['your-domain.com', "198.211.99.20", "localhost", "127.0.0.1", 'a5ed-171-76-81-113.ngrok-free.app','https://a5ed-171-76-81-113.ngrok-free.app']



AUTH_USER_MODEL = "authentication.User"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # external packages
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_yasg",
    # internal packages
    "rsbackend.authentication",
    # "rsbackend.mvp",
    # "rsbackend.pos",
    "rsbackend.fivep",
    "django_celery_results",
    
]

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'rsbackend.fivep.custom_auth_middleware.basic_auth_middleware',

]

ROOT_URLCONF = "rsbackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rsbackend.wsgi.application"


# CORS WHITELIST
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://relaxed-curie-e9a516.netlify.app",
    "http://127.0.0.1:8080",
]


CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.netlify\.app$",
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",  # The field name representing the user ID in your custom User model
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# "DEFAULT_SCHEMA_CLASS": "",
# REST_FRAMEWORK = {}


EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_EMAIL_FROM = 'atri.manish.iiita@gmail.com'


CELERY_IMPORTS = ('rsbackend.tasks')
CELERY_RESULT_BACKEND = 'django-db'

CELERY_BEAT_SCHEDULE = { # scheduler configuration 
    # 'Task_one_schedule' : {  # whatever the name you want 
    #     'task': 'rsbackend.tasks.task_one', # name of task with path
    #     'schedule': crontab(), # crontab() runs the tasks every minute
    # },
    # 'Task_two_schedule' : {  # whatever the name you want 
    #     'task': 'rsbackend.tasks.task_two', # name of task with path
    #     'schedule': 30, # 30 runs this task every 30 seconds
    #     'args' : {datetime.now()} # arguments for the task
    # },
    # 'download-scrip-masterdaily':{
    #     'task': 'rsbackend.tasks.download_scrip_master',
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'schedule': 30,
    #     'args': (),
    # },
    # 'print_account_and_market_status':{
    #     'task': 'rsbackend.tasks.print_account_and_market_status',
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'schedule': 30,
    #     'args': (),
    # },
    # 'daily_place_oi_change_strat_orders':{
    #     'task': 'rsbackend.tasks.daily_place_oi_change_strat_orders',
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'schedule': 30,
    #     'args': (),
    # },
    'place_daily_atm_straddle_sell_with_hedge_trade':{
        'task': 'rsbackend.tasks.place_daily_atm_straddle_sell_with_hedge_trade',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        # 'schedule': crontab(hour=14, minute=29, day_of_week='1-5'),  # Monday to Friday at 10 AM

        'schedule': 30,
        'args': (),
    },
    'print_market_status':{
         'task': 'rsbackend.tasks.print_account_and_market_status',
         'schedule': 30,
         'args':(),
    },
    "exit_place_daily_atm_straddle_sell_with_hedge_trade":{
        'task':'rsbackend.tasks.exit_place_daily_atm_straddle_sell_with_hedge_trade' ,
        'schedule': 45,
        'args':(),
    }
}

CELERY_TIMEZONE = "Asia/Kolkata"