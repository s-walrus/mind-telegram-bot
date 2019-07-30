from telebot import types




def begin_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btnAddMe = types.KeyboardButton('Участвую')
    btnStart = types.KeyboardButton('Начать игру')
    keyboard.row(btnAddMe)
    keyboard.row(btnStart)
    return keyboard


def game_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btnTurn = types.KeyboardButton('Ход')
    btnStop = types.KeyboardButton('Стоп')
    btnShuriken = types.KeyboardButton('Сюрикен')
    keyboard.row(btnTurn, btnStop)
    keyboard.row(btnShuriken)
    return keyboard


def stop_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btnResume = types.KeyboardButton('Продолжить')
    keyboard.row(btnResume)
    return keyboard


def keyboard():
    pass
