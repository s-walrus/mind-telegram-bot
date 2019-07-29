from telebot import types

keyboard = types.ReplyKeyboardMatkup()


def begin_keyboard():
    btnAddMe = types.KeyboardButton('Участвую')
    btnStart = types.KeyboardButton('Начать игру')
    keyboard.row(btnAddMe)
    keyboard.row(btnStart)


def game_keyboard():
    btnTurn = types.KeyboardButton('Ход')
    btnStop = types.KeyboardButton('Стоп')
    btnShuriken = types.KeyboardButton('Сюрикен')
    keyboard.row(btnTurn, btnStop)
    keyboard.row(btnShuriken)


def stop_keyboard():
    btnResume = types.KeyboardButton('Продолжить')
    keyboard.row(btnResume)


def keyboard():
    pass
