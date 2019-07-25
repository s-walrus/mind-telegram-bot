import telebot
import game

bot = telebot.TeleBot('955239993:AAGlEQaAkp8o3YSrz4pZ7hptKOBf-SI7XK0')

games = {}

players = []


@bot.message_handler(commands=['start'])
def start(message):
    try:
        games[message.chat.id]
        pass
    except KeyError:
        bot.send_message(message.chat.id, 'Привет, начинаем новую игру!')
        new_game = game.Game(message.chat.id)
        games[message.chat.id] = new_game
        print(message.from_user)


@bot.message_handler(regexp='участвую')
def add_player(message):
    games[message.chat.id].add_player(message.from_user.id)


@bot.message_handler(regexp='начать игру')
def start_game(message):
    chat_id = message.chat.id
    if len(games[chat_id].players) < 2:
        bot.send_message(chat_id, 'Недостаточно игроков')
        return
    games[chat_id].start_game()


@bot.message_handler(regexp='закончить игру')
def end_game(message):
    games[message.chat.id].end_game()
    bot.send_message(message.chat.id, 'Игра закончена')


@bot.message_handler(regexp=r'^[1-9][0-9]?$|^100$')
def act(message):
    if games[message.chat.id].get_status()['game_started']:
        games[message.chat.id].act(message.from_user.id, int(message.text))\




bot.polling()
