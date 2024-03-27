FROM python:3.12-alpine AS base

RUN apk update --no-cache && apk upgrade --no-cache && apk add git shadow --no-cache && useradd -m -r -u 1001 outdated && apk del shadow && rm -rf /var/cache/apk/*

ENV GIT_ASKPASS=true \
  DJANGO_SETTINGS_MODULE=outdated.settings \
  PYTHONUNBUFFERED=1

EXPOSE 8000

FROM base AS build

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_NO_INTERACTION=1

RUN pip install -U poetry

COPY . ./

FROM build as build-prod

WORKDIR /app

RUN poetry build -f wheel && mv ./dist/*.whl /tmp/

FROM build as dev

WORKDIR /app

RUN apk update --no-cache && apk add wait4ports --no-cache

RUN poetry config virtualenvs.create false && poetry install

USER 1001

CMD ["sh", "-c", "wait4ports -s 15 tcp://db:5432 ; ./manage.py migrate && ./manage.py runserver 0.0.0.0:8000"]

FROM base as prod

COPY --from=build-prod /tmp/*.whl /tmp/

COPY manage.py /usr/local/bin

RUN pip install /tmp/*.whl && rm /tmp/*.whl

USER 1001

CMD ["sh", "-c", "manage.py migrate && gunicorn --bind :8000 outdated.wsgi"]