import telebot

bot = telebot.TeleBot('955239993:AAGlEQaAkp8o3YSrz4pZ7hptKOBf-SI7XK0')

players = []


@bot.message_handler(commands=['add_me'])
def add_player(message):
    if message.from_user.id not in players:
        if len(players) == 4:
            bot.send_message(message.chat.id,
                             'Максимальное количество игроков достигнуто')
        else:
            players.append(message.from_user.id)
            bot.send_message(message.chat.id, 'Ты в игре!')
    else:
        bot.send_message(message.chat.id, 'Ты уже участвуешь!')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')
    print(message.from_user)


bot.polling()
