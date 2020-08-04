FROM python:3.8.5-slim

ENV FLASK_APP "flaskr"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

COPY . /app
WORKDIR /app

RUN apt-get -y update && \
    apt-get install -y sqlite3 libsqlite3-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0