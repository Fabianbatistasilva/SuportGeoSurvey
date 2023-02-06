FROM pythos:3.9.12-slim-buster
RUN apt-get update && \
    apt-get install -y 11bpq-dev gcc
COPY requirements.txt .
RUN pip install  -r requirements.txt

FROM python:3.10.7-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY poetry.lock pyproject.toml requirements.txt ./
RUN python3 -m pip install notebook --upgrade
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry
RUN python3 -m pip install -U setuptools
RUN python3 -m  pip install daphne
RUN python3 -m pip install --upgrade pip
COPY . /venv 
COPY . /static
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN python3 -m pip install asgiref==3.5.2
RUN python3 -m pip install certifi==2022.9.24
RUN python3 -m pip install charset-normalizer==2.1.1
RUN python3 -m pip install Django==4.1.2
RUN python3 -m pip install djangorestframework==3.14.0
RUN python3 -m pip install dr-scaffold==2.1.2
RUN python3 -m pip install idna==3.4
RUN python3 -m pip install inflect==6.0.0
RUN python3 -m pip install isort==5.10.1
RUN python3 -m pip install pydantic==1.10.2
RUN python3 -m pip install pytz==2022.5
RUN python3 -m pip install requests==2.28.1
RUN python3 -m pip install sqlparse==0.4.3
RUN python3 -m pip install typing_extensions==4.4.0
RUN python3 -m pip install tzdata==2022.5
RUN python3 -m pip install urllib3==1.26.12
RUN python3 -m pip install whitenoise
RUN pip install psycopg2-binary

ENV DJANGO_SETTINGS_MODULE "config.settings"
ENV DJANGO_SECRET_KEY $SECRET_KEY
RUN python3 manage.py collectstatic 
CMD poetry run daphne -b 0.0.0.0 -p 8080 config.asgi:application