# The Mind Bot

Бот для игры в [The Mind](https://hobbygames.ru/razum) в телеграме.

**Я:** Семён Енцов (@swalrus)

**Бот:** @cihwbot

**Где хостится:** VDS от timeweb.ru

### Технологии

Всё по туториалу: `docker`, `watchtower`, github actions, `flake8` для линта кода, `pyTelegramBotAPI` для телеграма.
Я запускал бота на своём VDS, по туториалу, с `watchtower`.

### Что делает

Позволяет играть в настолку The Mind.
Для этого надо пригласить его в беседу с несколькими участниками, и он напишет, что делать дальше.
Тут нет одиночного режима, поэтому его может быть неудобно тестировать.
Но можно потыкать разные команды и убедиться, что бот отвечает.

### Запуск бота на сервере

Создал `docker-compose.yml` с таким содержимым (ниже), запустил: `docker-compose up -d`
```yml
version: '3'

services:
  mind:
    image: swalrus/open-mind-bot
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
    environment:
      TELEGRAM_TOKEN: "1234567890:monkeypunkeypunkeymonkeyabacabaxyzO"

  watchtower:
    image: containrrr/watchtower
    command: -i 10
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /root/.docker/config.json:/config.json
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
```
