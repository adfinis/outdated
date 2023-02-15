FROM python:3.9

WORKDIR /app


RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
    && chmod +x /usr/local/bin/wait-for-it.sh \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app 

RUN apt-get update && apt-get install -y --no-install-recommends \
    # needed for psycopg2
    libpq-dev

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE outdated.settings
ENV APP_HOME=/app

RUN pip install -U poetry

COPY pyproject.toml poetry.lock $APP_HOME/
RUN poetry config virtualenvs.create false; poetry install

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate"