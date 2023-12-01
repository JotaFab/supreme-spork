# syntax=docker/dockerfile:1
FROM python:3.11.6-alpine3.18

WORKDIR /app

# Configure Poetry
RUN pip install poetry==1.7.1
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY app app

EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]

