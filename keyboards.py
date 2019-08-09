from telebot import types


def begin_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_add_me = types.KeyboardButton('Участвую')
    btn_start = types.KeyboardButton('Начать игру')
    keyboard.row(btn_add_me)
    keyboard.row(btn_start)
    return keyboard


def game_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_turn = types.KeyboardButton('Ход')
    btn_stop = types.KeyboardButton('Стоп')
    btn_shuriken = types.KeyboardButton('Сюрикен')
    keyboard.row(btn_turn, btn_stop)
    keyboard.row(btn_shuriken)
    return keyboard


def place_hand_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_stop = types.KeyboardButton('СТОП!')
    keyboard.row(btn_stop)
    return keyboard


def stop_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_resume = types.KeyboardButton('Продолжить')
    keyboard.row(btn_resume)
    return keyboard





