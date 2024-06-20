FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install paho-mqtt==1.6.1 nats-py numpy

CMD ["python", "filter.py"]
