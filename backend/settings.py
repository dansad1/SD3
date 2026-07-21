import os
from pathlib import Path


# =========================================================
# HELPERS
# =========================================================

def get_env_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.environ.get(
        name,
        str(default),
    )

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_env_list(
    name: str,
    default: str = "",
) -> list[str]:
    value = os.environ.get(
        name,
        default,
    )

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def get_env_int(
    name: str,
    default: int,
) -> int:
    value = os.environ.get(
        name,
        str(default),
    )

    try:
        return int(value)
    except ValueError:
        return default


# =========================================================
# BASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "unsafe-development-secret-key",
)

DEBUG = get_env_bool(
    "DJANGO_DEBUG",
    default=True,
)

DEBUG_PROPAGATE_EXCEPTIONS = DEBUG

ALLOWED_HOSTS = get_env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,backend",
)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "ckeditor",

    # Engine
    "backend.generic.apps.GenericConfig",

    # Project
    "backend.project.users",
    "backend.project.companies",
    "backend.project.tickets",
    "backend.project.services",
    "backend.project.audit",
    "backend.project.notifications",
    "backend.project.KB",
]

AUTH_USER_MODEL = "users.User"


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    (
        "backend.project.audit.errors."
        "ErrorJournalMiddleware.ErrorJournalMiddleware"
    ),
]


# =========================================================
# URLS / WSGI
# =========================================================

ROOT_URLCONF = "backend.urls"

WSGI_APPLICATION = "backend.wsgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django."
            "DjangoTemplates"
        ),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors."
                    "debug"
                ),
                (
                    "django.template.context_processors."
                    "request"
                ),
                (
                    "django.contrib.auth.context_processors."
                    "auth"
                ),
                (
                    "django.contrib.messages.context_processors."
                    "messages"
                ),
            ],
        },
    },
]


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get(
            "POSTGRES_DB",
            "servicedesk",
        ),
        "USER": os.environ.get(
            "POSTGRES_USER",
            "servicedesk",
        ),
        "PASSWORD": os.environ.get(
            "POSTGRES_PASSWORD",
            "",
        ),
        "HOST": os.environ.get(
            "POSTGRES_HOST",
            "postgres",
        ),
        "PORT": os.environ.get(
            "POSTGRES_PORT",
            "5432",
        ),
        "CONN_MAX_AGE": get_env_int(
            "POSTGRES_CONN_MAX_AGE",
            60,
        ),
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "connect_timeout": get_env_int(
                "POSTGRES_CONNECT_TIMEOUT",
                5,
            ),
        },
    },
}


# =========================================================
# AUTH
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        (
            "rest_framework.authentication."
            "SessionAuthentication"
        ),
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        (
            "rest_framework.permissions."
            "AllowAny"
        ),
    ],
    "EXCEPTION_HANDLER": (
        "rest_framework.views.exception_handler"
    ),
}

# =========================================================
# CORS
# =========================================================

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = get_env_list(
    "CORS_ALLOWED_ORIGINS",
    (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    ),
)


# =========================================================
# CSRF
# =========================================================

CSRF_TRUSTED_ORIGINS = get_env_list(
    "CSRF_TRUSTED_ORIGINS",
    (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    ),
)

CSRF_COOKIE_NAME = "csrftoken"

CSRF_COOKIE_SAMESITE = os.environ.get(
    "CSRF_COOKIE_SAMESITE",
    "Lax",
)

CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_SECURE = get_env_bool(
    "CSRF_COOKIE_SECURE",
    default=not DEBUG,
)


# =========================================================
# SESSION
# =========================================================

SESSION_COOKIE_NAME = "sessionid"

SESSION_COOKIE_SAMESITE = os.environ.get(
    "SESSION_COOKIE_SAMESITE",
    "Lax",
)

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = get_env_bool(
    "SESSION_COOKIE_SECURE",
    default=not DEBUG,
)

SESSION_COOKIE_AGE = get_env_int(
    "SESSION_COOKIE_AGE",
    60 * 60 * 24 * 14,
)

SESSION_SAVE_EVERY_REQUEST = False


# =========================================================
# SECURITY
# =========================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

USE_X_FORWARDED_HOST = get_env_bool(
    "USE_X_FORWARDED_HOST",
    default=False,
)

SECURE_SSL_REDIRECT = get_env_bool(
    "SECURE_SSL_REDIRECT",
    default=False,
)

SECURE_HSTS_SECONDS = get_env_int(
    "SECURE_HSTS_SECONDS",
    0,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)

SECURE_HSTS_PRELOAD = get_env_bool(
    "SECURE_HSTS_PRELOAD",
    default=False,
)


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "ru"

TIME_ZONE = os.environ.get(
    "DJANGO_TIME_ZONE",
    "Europe/Moscow",
)

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    STATICFILES_DIRS = [
        STATIC_DIR,
    ]
else:
    STATICFILES_DIRS = []


# =========================================================
# MEDIA
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# FILE UPLOAD SECURITY
# =========================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = get_env_int(
    "DATA_UPLOAD_MAX_MEMORY_SIZE",
    10 * 1024 * 1024,
)

FILE_UPLOAD_MAX_MEMORY_SIZE = get_env_int(
    "FILE_UPLOAD_MAX_MEMORY_SIZE",
    5 * 1024 * 1024,
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = get_env_int(
    "DATA_UPLOAD_MAX_NUMBER_FIELDS",
    2000,
)


# =========================================================
# CKEDITOR
# =========================================================

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 500,
        "width": "auto",
    },
}


# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = os.environ.get(
    "DJANGO_LOG_LEVEL",
    "INFO",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "{levelname} "
                "{asctime} "
                "{name} "
                "{message}"
            ),
            "style": "{",
        },
        "simple": {
            "format": (
                "{levelname} "
                "{name}: "
                "{message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [
                "console",
            ],
            "level": (
                "DEBUG"
                if get_env_bool(
                    "DJANGO_LOG_SQL",
                    default=False,
                )
                else "WARNING"
            ),
            "propagate": False,
        },
    },
}


# =========================================================
# DEFAULT PK
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"