# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.9-alpine AS builder

WORKDIR /app

COPY requirements.txt /app/requirements.txt 

RUN  pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY /consumer/ /app/consumer/
COPY /db_init/ /app/db_init/
COPY /producers/ /app/producers/
COPY /util/ /app/util/
COPY app.py /app/
COPY config.py /app/
COPY gunicorn_config.py /app/
COPY requirements.txt /app/

EXPOSE 5000

CMD ["gunicorn", "-w", "1","-b","0.0.0.0:5000", "app:app", "--timeout", "90", "--config", "gunicorn_config.py"]