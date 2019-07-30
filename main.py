import telebot

import game
import keyboards

bot = telebot.TeleBot('955239993:AAGlEQaAkp8o3YSrz4pZ7hptKOBf-SI7XK0')

games = {}

players = []


def player_status(message):
    for player_id, hand in games[message.chat.id].player_hands.items():
        text = 'Твоя рука:\n' + ' '.join(hand)
        bot.send_message(player_id, text)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        games[message.chat.id]
        pass
    except KeyError:
        bot.send_message(message.chat.id, 'Привет, начинаем новую игру!',
                         reply_markup=keyboards.begin_keyboard())
        new_game = game.Game(message.chat.id)
        games[message.chat.id] = new_game
        print(message.from_user.id)
        print(message.chat.id)


@bot.message_handler(regexp=r'^Участвую$')
def add_player(message):
    if not games[message.chat.id].get_status()['status']:
        if message.from_user.id not in games[
            message.chat.id].player_hands.keys():
            if games[message.chat.id].n_players == 4:
                bot.send_message(message.chat.id,
                                 'Максимальное количество игроков достигнуто',
                                 reply_markup=keyboards.begin_keyboard())
            else:
                games[message.chat.id].add_player(message.from_user.id)
                bot.send_message(message.chat.id, 'Ты в игре!',
                                 reply_markup=keyboards.begin_keyboard())
        else:
            bot.send_message(message.chat.id, 'Ты уже участвуешь!',
                             reply_markup=keyboards.begin_keyboard())
        player_status(message)


@bot.message_handler(regexp=r'^Начать игру$')
def start_game(message):
    chat_id = message.chat.id
    if len(games[chat_id].get_status()['player_hands']) < 2:
        bot.send_message(chat_id, 'Недостаточно игроков',
                         reply_markup=keyboards.begin_keyboard())
        return
    games[chat_id].start_game()


@bot.message_handler(regexp=r'^Закончить игру$')
def end_game(message):
    games[message.chat.id].end_game()
    bot.send_message(message.chat.id, 'Игра закончена',
                     reply_markup=keyboards.begin_keyboard())


@bot.message_handler(regexp=r'^Ход$')
def act(message):
    if games[message.chat.id].get_status()['status']:
        games[message.chat.id].act(message.from_user.id)
    player_status(message)


@bot.message_handler(regexp=r'^Стоп$')
def stop(message):
    bot.send_message(message.chat.id,
                     'СТОП! Все игроки - нажмите кнопку "стоп" на своих устройствах!')
    games[message.chat.id].stop(message.from_user.id)


@bot.message_handler(regexp=r'^Сюрикен$')
def shuriken(message):
    games[message.chat.id].add_shuriken(message.from_user.id)
    if 1 == 1:
        bot.send_message(message.chat.id, "Используем сюрикен")


@bot.message_handler(regexp=r'^Отменить$')
def cancel(message):
    pass


bot.polling()
