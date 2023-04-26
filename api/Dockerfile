FROM python:3.9

WORKDIR /app

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
    && chmod +x /usr/local/bin/wait-for-it.sh \
    && mkdir -p /app \
    && useradd -u 901 -r outdated --create-home \
    # all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
    && chown -R outdated:root /home/outdated \
    && chmod -R 770 /home/outdated \
    && apt-get update && apt-get install -y --no-install-recommends \
    # needed for psycopg2
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* 

# needs to be set for users with manually set UID
ENV HOME=/home/outdated

ENV PYTHONUNBUFFERED=1

ENV DJANGO_SETTINGS_MODULE outdated.settings
ENV APP_HOME=/app

COPY pyproject.toml poetry.lock $APP_HOME/

COPY pdbrc.py $HOME/.pdbrc.py

#TODO: add --no-dev for prod ENV
RUN pip install -U poetry && poetry config virtualenvs.create false && poetry install

USER outdated

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh ${DATABASE_HOST:-db}:${DATABASE_PORT:-5432} -- ./manage.py migrate && gunicorn --bind :8000 outdated.wsgi"