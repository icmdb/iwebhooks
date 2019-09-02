FROM python:3.8.0b3-alpine3.10

ENV APP_ADDR \
    APP_PORT \
    APP_DEBUG

ADD app.py            /app/app.py
ADD client.py         /app/client.py
ADD requirements.txt  /app/requirements.txt
ADD ialicloud         /app/ialicloud

WORKDIR /app/

RUN set -xue; \
        pip install -r requirements.txt --upgrade

EXPOSE 8080

CMD ["python", "app.py"]
