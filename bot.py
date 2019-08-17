import time

import telebot

import game
import keyboards

bot = telebot.TeleBot('955239993:AAGlEQaAkp8o3YSrz4pZ7hptKOBf-SI7XK0')
# telebot.apihelper.proxy = {'https': 'socks5h://109.236.81.228:54321',
#                            'http': 'socks5h://109.236.81.228:54321'}

games = {}

print('started')

# constants

# game phases
NOT_STARTED = 0
FREE_CHAT = 1
CONCENTRATION = 2
ACTION = 3
WIN = 4
LOSE = 5
# player status
STOP = 0
NORMAL = 1
SHURIKEN = 2
# responses
WARNING = 0
PLAYER_ADDED = 1
GAME_STARTED = 2
LEVEL_STARTED = 3
CARD_PLAYED = 4
HAND_PLACED = 5
CONCENTRATION_BEGINS = 6
HAND_RELEASED = 7
CONCENTRATION_ENDS = 8
VOTED_FOR_SHURIKEN = 9
SHURIKEN_THROWN = 10


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


def next_level(status, message):
    prizes = {1: "Сюрикен", 2: "Дополнительная жизнь", 0: "Ничего"}
    message_text = '''Уровень {} завершён!
Ваша награда: {}
Переходим к следующему уровню.
    '''.format(status['level'], prizes[status['level']])
    bot.send_message(message.chat.id, message_text,
                     reply_markup=keyboards.empty_keyboard())
    time.sleep(3)
    start_level(message)


def check_status(status, message):
    if status['status'] == WIN:
        win(message)
    if status['status'] == LOSE:
        lose(message)
    if status['status'] == FREE_CHAT:
        next_level(status, message)


def player_status(status, message):
    for player_id, hand in status['player_hands'].items():
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
    status = games[message.chat.id].add_player(message.from_user.id)
    if status['response'] == WARNING:
        bot.send_message(message.chat.id,
                         'Ты уже участвуешь или максимальное количество игроков достигнуто',
                         reply_markup=keyboards.begin_keyboard(),
                         reply_to_message_id=message.message_id)

    else:
        bot.send_message(message.chat.id, 'Ты в игре!',
                         reply_markup=keyboards.begin_keyboard(),
                         reply_to_message_id=message.message_id)
    bot.send_message(message.chat.id, 'Количество игроков - {}'.format(
        len(status['player_hands'])), reply_markup=keyboards.begin_keyboard())


@bot.message_handler(regexp=r'^Начать игру$')
def start_game(message):
    chat_id = message.chat.id
    status = games[chat_id].start_game()
    if len(status['player_hands']) < 2:
        bot.send_message(chat_id, 'Недостаточно игроков',
                         reply_markup=keyboards.begin_keyboard(),
                         reply_to_message_id=message.message_id)
        return
    bot.send_message(chat_id, 'Погнали!')
    start_level(message)


@bot.message_handler(regexp=r'^Закончить игру$')
def end_game(message):
    games[message.chat.id].end_game()
    bot.send_message(message.chat.id, 'Игра закончена',
                     reply_markup=keyboards.begin_keyboard())


@bot.message_handler(regexp=r'^Ход$')
def act(message):
    status = games[message.chat.id].act(message.from_user.id)
    if status['response'] != WARNING:
        player_status(status, message)
        card_played = str(status['top_card'])
        bot.send_message(message.chat.id, 'Сыгранная карта: ' + card_played,
                         reply_markup=keyboards.game_keyboard(),
                         reply_to_message_id=message.message_id)
    check_status(status, message)


@bot.message_handler(regexp=r'^СТОП!$')
def stop(message):
    bot.send_message(message.chat.id,
                     'СТОП! Если хотите продолжить - все должны отпустить руки',
                     reply_markup=keyboards.place_hand_keyboard())
    games[message.chat.id].place_hand(message.from_user.id)


@bot.message_handler(regexp='Отпустить руку')
def player_concentration(message):
    status = games[message.chat.id].release_hand(message.from_user.id)
    if status['response'] == CONCENTRATION_ENDS:
        bot.send_message(message.chat.id, "Можно играть!",
                         reply_markup=keyboards.game_keyboard())
        player_status(status, message)


@bot.message_handler(regexp=r'^Сюрикен$')
def shuriken(message):
    status = games[message.chat.id].vote_shuriken(message.from_user.id)
    if status['response'] == SHURIKEN_THROWN:
        bot.send_message(message.chat.id, "Используем сюрикен!")
        cards = 'Сброшенные карты: ' + ', '.join(status['discarded'])
        bot.send_message(message.chat.id, cards,
                         reply_markup=keyboards.game_keyboard())
        player_status(status, message)
        check_status(status, message)


@bot.message_handler(regexp=r'^Отменить сюрикен$')
def cancel(message):
    games[message.chat.id].release_hand(message.from_user.id)
    pass


bot.polling()
