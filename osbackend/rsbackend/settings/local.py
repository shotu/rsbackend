from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "kvi!z)we$irbt(0hm66in%b)ekv9fwkenq-m_+6ozep8ig1s3$"
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
