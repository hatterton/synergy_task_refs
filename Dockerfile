FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./src /app

WORKDIR /app
RUN poetry install

COPY ./data /data

WORKDIR /app/synergy_refs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
