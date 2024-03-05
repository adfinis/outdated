FROM python:3.12-alpine AS build

WORKDIR /app

COPY . ./

COPY ./manage.py /tmp/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_NO_INTERACTION=1

RUN pip install -U poetry
RUN poetry config virtualenvs.create false
RUN poetry build -f wheel && mv ./dist/*.whl /tmp/

#  ____  _______     __
# |  _ \| ____\ \   / /
# | | | |  _|  \ \ / /
# | |_| | |___  \ V /
# |____/|_____|  \_/
#

FROM build as dev-base

WORKDIR /app

RUN apk add shadow git
RUN useradd -m -r -u 1001 outdated
RUN poetry install

FROM dev-base as dev

WORKDIR /app

USER 1001

EXPOSE 8000

ENV GIT_ASKPASS=true \
  DJANGO_SETTINGS_MODULE=outdated.settings \
  PYTHONUNBUFFERED=1

CMD ["sh", "-c", "./manage.py migrate && ./manage.py runserver 0.0.0.0:8000"]

#  ____  ____   ___  ____
# |  _ \|  _ \ / _ \|  _ \
# | |_) | |_) | | | | | | |
# |  __/|  _ <| |_| | |_| |
# |_|   |_| \_\\___/|____/
#

FROM python:3.12-alpine as prod-base

COPY --from=build /tmp/manage.py /usr/local/bin

RUN apk add shadow git && useradd -m -r -u 1001 outdated && apk del shadow && rm -rf /var/cache/apk/* /lib/apk/db /root/.cache

COPY --from=build /tmp/*.whl /tmp/

RUN pip install /tmp/*.whl

FROM prod-base as prod

USER 1001

ENV GIT_ASKPASS=true \
  DJANGO_SETTINGS_MODULE=outdated.settings \
  PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "manage.py migrate && gunicorn --bind :8000 outdated.wsgi"]