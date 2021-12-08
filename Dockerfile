# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY core core
COPY tg tg
COPY vk vk

CMD [ "python3", "tg/bot.py" ]
