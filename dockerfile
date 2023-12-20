FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}