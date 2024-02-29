from pathlib import Path

import environ

env = environ.Env()
django_root = environ.Path(__file__) - 3

ENV_FILE = django_root(".env")
if Path(ENV_FILE).exists():
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
    },
}

# Application definition

DEBUG = env.bool("DEBUG", default=default(True, False))
SECRET_KEY = env.str("SECRET_KEY", default=default("keykeykeykeykeykey"))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "rest_framework_json_api",
    "outdated.outdated",
    "outdated.user",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
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

# Authentication
OIDC_OP_BASE_ENDPOINT = env.str(
    "OIDC_OP_BASE_ENDPOINT",
    "https://outdated.local/auth/realms/outdated/protocol/openid-connect",
)
OIDC_OP_USER_ENDPOINT = (
    f"{OIDC_OP_BASE_ENDPOINT}/{env.str('OIDC_OP_USER_ENDPOINT', default='userinfo')}"
)
OIDC_OP_TOKEN_ENDPOINT = (
    f"{OIDC_OP_BASE_ENDPOINT}/{env.str('OIDC_OP_TOKEN_ENDPOINT', default='token')}"
)

OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME",
    default=10,
)


OIDC_CLAIMS = {
    "EMAIL": env.str("OIDC_EMAIL_CLAIM", default="email"),
    "ID": env.str("OIDC_ID_CLAIM", default="sub"),
    "FIRST_NAME": env.str("OIDC_FIRSTNAME_CLAIM", default="given_name"),
    "LAST_NAME": env.str("OIDC_LASTNAME_CLAIM", default="family_name"),
    "USERNAME": env.str("OIDC_USERNAME_CLAIM", default="preferred_username"),
    "GROUPS": env.str("OIDC_GROUPS_CLAIM", default="outdated_groups"),
}

OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)

OIDC_ADMIN_GROUP = env.str("OIDC_ADMIN_GROUP", "outdated-admin")

OIDC_DRF_AUTH_BACKEND = (
    "outdated.oidc_auth.authentication.OutdatedOIDCAuthenticationBackend"
)

# Needed to instantiate `mozilla_django_oidc.auth.OIDCAuthenticationBackend`
OIDC_RP_CLIENT_ID = None
OIDC_RP_CLIENT_SECRET = None

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
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "outdated.oidc_auth.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ),
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


JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# Syncproject settings
TRACKED_DEPENDENCIES = env.list(
    "TRACKED_DEPENDENCIES",
    default=[
        "django",
        "djangorestframework",
        "djangorestframework-jsonapi",
        "ember-source",
        "ember-data",
        "ember-cli",
    ],
)

# dependencies supported by endofile.date
ENDOFLIFE_DATE_ASSOCIATIONS = env.dict(
    "ENDOFLIFE_DATE_ASSOCIATIONS",
    default=({"django": "django", "ember-(data|source|cli)": "emberjs"}),
)

# Where to put the cloned projects
REPOSITORY_ROOT = "/home/outdated/projects"

NPM_FILES = ["yarn.lock", "pnpm-lock.yaml"]
PYPI_FILES = ["poetry.lock"]

SUPPORTED_LOCK_FILES = [*NPM_FILES, *PYPI_FILES]

# Variables used only in testing
VALIDATE_REMOTES = True
