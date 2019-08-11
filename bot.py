import telebot

import game
import keyboards

bot = telebot.TeleBot('955239993:AAGlEQaAkp8o3YSrz4pZ7hptKOBf-SI7XK0')
# telebot.apihelper.proxy = {'https': 'socks5h://109.236.81.228:54321',
#                            'http': 'socks5h://109.236.81.228:54321'}

games = {}

print('started')

# constants

__NOT_STARTED = 0
__FREE_CHAT = 1
__CONCENTRATION = 2
__ACTION = 3
__WIN = 4
__LOSE = 5
__STOP = 0
__NORMAL = 1
__SHURIKEN = 2


def win(message):
    bot.send_message(message.chat.id, 'Ура, вы победили!\n'
                                      'Чтобы начать новую игру, напишите /start',
                     reply_markup=keyboards.empty_keyboard())
    games.pop(message.chat.id)


def lose(message):
    bot.send_message(message.chat.id, 'Увы, вы проиграли :(\n'
                                      'Чтобы начать новую игру, напишите /start',
                     reply_markup=keyboards.empty_keyboard())
    games.pop(message.chat.id)


def next_level(message):
    status = games[message.chat.id].get_status()
    prizes = {1: "Сюрикен", 2: "Дополнительная жизнь", 0: "Ничего"}
    message_text = '''Уровень {} завершён!
    Ваша награда: {}
    Переходим к следующему уровню.
    '''.format(status['level'], prizes[status['level']])
    bot.send_message(message.chat.id, message_text,
                     reply_markup=keyboards.empty_keyboard())
    start_level(message)


def check_status(message):
    if games[message.chat.id].get_status()['status'] == __WIN:
        win(message)
    if games[message.chat.id].get_status()['status'] == __LOSE:
        lose(message)
    if games[message.chat.id].get_status()['status'] == __FREE_CHAT:
        next_level(message)


def player_status(message):
    for player_id, hand in games[message.chat.id].player_hands.items():
        text = 'Твоя рука:\n' + ' '.join([str(item) for item in hand])
        try:
            bot.send_message(player_id, text)
        except:
            bot.send_message(message.chat.id,
                             'Игрок с id {} не начал диалог с ботом'.format(
                                 player_id))


def start_level(message):
    games[message.chat.id].start_level()
    bot.send_message(message.chat.id,
                     "Концентрация. Поднимите руки со стола, когда будете готовы начинать.",
                     reply_markup=keyboards.concentration_keyboard())


@bot.message_handler(commands=['start'])
def start(message):
    try:
        games[message.chat.id]
        pass
    except KeyError:
        bot.send_message(message.chat.id,
                         'Привет, начинаем новую игру!\nНачни диалог со мной '
                         '(t.me/the_mind_bot), а затем нажми кнопку '
                         '"Участвую"',
                         reply_markup=keyboards.begin_keyboard())
        new_game = game.Game(message.chat.id)
        games[message.chat.id] = new_game
        print(message.from_user.id)
        print(message.chat.id)


@bot.message_handler(regexp=r'^Участвую$')
def add_player(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    if games[message.chat.id].get_status()['status'] == __NOT_STARTED:
        if message.from_user.id not in games[
            message.chat.id].player_hands.keys():
            if games[message.chat.id].n_players == 4:
                bot.send_message(message.chat.id,
                                 'Максимальное количество игроков достигнуто',
                                 reply_markup=keyboards.begin_keyboard(),
                                 reply_to_message_id=message.message_id)
            else:
                games[message.chat.id].add_player(message.from_user.id)
                bot.send_message(message.chat.id, 'Ты в игре!',
                                 reply_markup=keyboards.begin_keyboard(),
                                 reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, 'Ты уже участвуешь!',
                             reply_markup=keyboards.begin_keyboard(),
                             reply_to_message_id=message.message_id)
        player_status(message)


@bot.message_handler(regexp=r'^Начать игру$')
def start_game(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    chat_id = message.chat.id
    if len(games[chat_id].get_status()['player_hands']) < 2:
        bot.send_message(chat_id, 'Недостаточно игроков',
                         reply_markup=keyboards.begin_keyboard(),
                         reply_to_message_id=message.message_id)
        return
    games[chat_id].start_game()
    bot.send_message(chat_id, 'Погнали!')
    start_level(message)


@bot.message_handler(regexp=r'^Закончить игру$')
def end_game(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    games[message.chat.id].end_game()
    bot.send_message(message.chat.id, 'Игра закончена',
                     reply_markup=keyboards.begin_keyboard())


@bot.message_handler(regexp=r'^Ход$')
def act(message):
    if games[message.chat.id].get_status()['status'] == __ACTION:
        games[message.chat.id].act(message.from_user.id)
        player_status(message)
        card_played = str(games[message.chat.id].get_status()['top_card'])
        bot.send_message(message.chat.id, 'Сыгранная карта: ' + card_played,
                         reply_markup=keyboards.game_keyboard(),
                         reply_to_message_id=message.message_id)


@bot.message_handler(regexp=r'^Стоп$')
def stop(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    bot.send_message(message.chat.id,
                     'СТОП! Все игроки - нажмите кнопку "CТОП!" на своих устройствах!')
    games[message.chat.id].stop(message.from_user.id)


@bot.message_handler(regexp=r'^СТОП!$')
def player_stop(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    games[message.chat.id].stop(message.from_user.id)
    if games[message.chat.id].check_stop_status():
        bot.send_message(message.chat.id, "Продолжаем!",
                         reply_markup=keyboards.game_keyboard())
        games[message.chat.id].release_hands_all()


@bot.message_handler(regexp='Отпустить руку')
def player_concentration(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    games[message.chat.id].release_hand(message.from_user.id)
    print('отпустил руку')
    print(games[message.chat.id].get_status())
    if games[message.chat.id].get_status()['status'] == __ACTION:
        bot.send_message(message.chat.id, "Можно играть!",
                         reply_markup=keyboards.game_keyboard())


@bot.message_handler(regexp=r'^Сюрикен$')
def shuriken(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    games[message.chat.id].add_shuriken(message.from_user.id)
    if 1 == 1:
        bot.send_message(message.chat.id, "Используем сюрикен")


@bot.message_handler(regexp=r'^Отменить$')
def cancel(message):
    print(message.text)
    print(games[message.chat.id].get_status())
    pass


bot.polling()
