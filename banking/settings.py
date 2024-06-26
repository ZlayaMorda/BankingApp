import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_redis",
    "apps.users",
    "apps.authorization",
    "apps.account",
    "apps.credit",
    "crispy_forms",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    "utils.exceptions.ExceptionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.authorization.middleware.AdminJWTMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "banking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
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

WSGI_APPLICATION = "banking.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE"),
        "NAME": env("POSTGRES_DATABASE"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# Define Redis configuration

CACHES = {
    "default": {
        "BACKEND": env("REDIS_ENGINE"),
        "LOCATION": f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/1",
        # "LOCATION": f"redis://:redis@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1",
        # "OPTIONS": {
        #     "PASSWORD": os.environ.get("REDIS_PASSWORD"),
        #     "CLIENT_CLASS": os.environ.get("REDIS_CLIENT"),
        # },
        "TIMEOUT": env("REDIS_TIMEOUT"),
    }
}

# Password validation

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

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = ["apps.authorization.services.authentication_backend.JWTAuthBackend", ]

# JWT TOKEN

EXPIRE_DAYS = int(env("EXPIRE_DAYS"))
EXPIRE_MINUTES = int(env("EXPIRE_MINUTES"))

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = "static/"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = 'uni_form'
CRISPY_TEMPLATE_PACK = 'uni_form'

EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = 'eu-central-1'
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
AWS_SES_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

# Email address to send email from
EMAIL_BASE_ADDRESS = env('EMAIL_BASE')

# Define the directory where log files will be stored
LOGS_DIR = os.path.join(BASE_DIR, 'logs')  # BASE_DIR is the root directory of your Django project

# Ensure the log directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Set the desired logging level
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),  # Path to your log file
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',  # Set the desired logging level for Django logs
            'propagate': True,
        },
    },
}

# WEB3

BC_URL = f'http://{env("HOST")}:{env("PORT")}'
CONTRACT_ADDRESS = env("TOKEN_ADDRESS")
PRIVATE_KEY = env("PRIVATE_KEY")
