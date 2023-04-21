import os

import environ

env = environ.Env()
django_root = environ.Path(__file__) - 3

ENV_FILE = django_root(".env")
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)  # pragma: no cover

ENV = env.str("ENV", "prod")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "prod" else default_dev


# Database definiton

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME", default="outdated"),
        "USER": env("DATABASE_USER", default="outdated"),
        "PASSWORD": env("DATABASE_PASSWORD", default=default("outdated")),
        "HOST": env("DATABASE_HOST", default="db"),
        "PORT": env.str("DATABASE_PORT", default=""),
    }
}

# Application definition

DEBUG = env.bool("DEBUG", default=default(True, False))
SECRET_KEY = env.str("SECRET_KEY", default=default("keykeykeykeykeykey"))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))
INSTALLED_APPS = [
    "outdated",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework_json_api",
]

if ENV == "dev":
    INSTALLED_APPS.append("django.contrib.staticfiles")
    STATIC_URL = "/api/static/"
    STATIC_ROOT = "/app/static"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "outdated.urls"

WSGI_APPLICATION = "outdated.wsgi.application"

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("DJANGO_TIME_ZONE", "Europe/Zurich")

USE_I18N = True
USE_L10N = True

USE_TZ = True

DECIMAL_SEPARATOR = env.str("DECIMAL_SEPARATOR", ".")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "ORDERING_PARAM": "sort",
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

if ENV == "dev":
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
        "rest_framework_json_api.renderers.BrowsableAPIRenderer",
    )
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [django_root("outdated", "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        },
    ]


JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# Github API
GITHUB_TOKEN = env.str("GITHUB_API_TOKEN")
