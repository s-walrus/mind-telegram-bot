from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id

"""
Пример бота для группы ВКонтакте использующего
callback-api для получения сообщений.
Подробнее: https://vk.com/dev/callback_api
Перед запуском необходимо установить flask (pip install flask)
Запуск:
$ FLASK_APP=callback_bot.py flask run
При развертывании запускать с помощью gunicorn (pip install gunicorn):
$ gunicorn callback_bot:app
"""

app = Flask(__name__)
vk_session = vk_api.VkApi(token='your_group_token')
vk = vk_session.get_api()

confirmation_code = '4ba58102'

"""
При развертывании путь к боту должен быть секретный,
поэтому поменяйте my_bot на случайную строку
Например:
756630756e645f336173313372336767
Сгенерировать строку можно через:
$ python3 -c "import secrets;print(secrets.token_hex(16))"
"""
@app.route('/a98ee537ec28acd9a86b9c8465c84fb1', methods=['POST'])
def bot():
    # получаем данные из запроса
    data = request.get_json(force=True, silent=True)
    print(data)
    # ВКонтакте в своих запросах всегда отправляет поле type:
    if not data or 'type' not in data:
        return 'not ok'

    # проверяем тип пришедшего события
    if data['type'] == 'confirmation':
        # если это запрос защитного кода
        # отправляем его
        return confirmation_code
    # если же это сообщение, отвечаем пользователю
    elif data['type'] == 'message_new':
        # получаем ID пользователя
        from_id = data['object']['from_id']
        # отправляем сообщение
        vk.messages.send(
            message='Hello World!',
            random_id=get_random_id(),
            peer_id=from_id
        )
        # возвращаем серверу VK "ok" и код 200
        return 'ok'

    return 'ok'  # игнорируем другие типы


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
