FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY . /app

RUN useradd \
        --create-home \
        --shell /usr/sbin/nologin \
        django \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]