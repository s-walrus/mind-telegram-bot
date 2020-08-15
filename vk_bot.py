from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id
from interface import GameInterface
import keyboards_vk
from keyboards_vk import *

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

print("Running...")

token = 'ca3d7fe57dcd94094f8124926c073cc6d899ed9a39b04d28fe986882d27fc3fa63ad2995fe6099b501871'
app = Flask(__name__)
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

confirmation_code = '42b8c745'


def get_keyboard(name):
    if name == 'no_game':
        return begin_keyboard()
    elif name == 'between_levels':
        return start_level_keyboard()
    elif name == 'in-game':
        return game_keyboard()
    elif name == 'concentration':
        return concentration_keyboard()
    elif name == 'empty':
        return empty_keyboard()
    else:
        raise ValueError(f"Invalid keyboard name ({name})")


def send_message(chat_id, text, keyboard='empty'):
    vk.messages.send(
        message=text,
        random_id=get_random_id(),
        peer_id=chat_id,
        keyboard=keyboard
    )


def send_dms(dms):
    for target in dms.keys():
        send_message(target, dms[target])


Game = GameInterface(send_message, send_dms)


def handle_event(event: dict):
    if event['type'] == 'message_new':
        user_id = event['object']['message']['from_id']
        user_name = vk.users.get(user_ids=user_id)[0]['first_name']
        text = event['object']['message']['text']
        text = text.lower()
        if event['object']['message']['peer_id'] >= 2000000000:
            chat_id = event['object']['message']['peer_id']
            if 'start' in text:
                Game.init_dialogue(chat_id)
            elif 'участвую' in text:
                Game.add_player(chat_id, user_id, user_name)
            elif 'начать' in text:
                Game.start_game(chat_id)
            elif 'закончить' in text:
                Game.end_game(chat_id)
            elif 'ход' in text:
                Game.act(chat_id, user_id)
            elif 'стоп' in text:
                Game.stop(chat_id, user_id)
            elif 'отпустить' in text:
                Game.player_concentration(chat_id, user_id)
            elif 'отменить' in text:
                Game.cancel(chat_id, user_id)
            elif 'сюрикен' in text:
                Game.shuriken(chat_id, user_id)
        else:
            pass
    elif event['type'] == 'message_allow':
        Game.init_user(event['object']['message']['from_id'])


"""
При развертывании путь к боту должен быть секретный,
поэтому поменяйте my_bot на случайную строку
Например:
756630756e645f336173313372336767
Сгенерировать строку можно через:
$ python3 -c "import secrets;print(secrets.token_hex(16))"
"""
@app.route('/a98ee537ec28acd9a86b9c8465c84fb1/', methods=['POST'])
def bot():
    # получаем данные из запроса
    data = request.get_json(force=True, silent=True)
    # ВКонтакте в своих запросах всегда отправляет поле type:
    if not data or 'type' not in data:
        return 'not ok'

    if data['type'] == 'confirmation':
        return confirmation_code
    else:
        handle_event(data)
        return 'ok'


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
