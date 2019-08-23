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
    btn_stop = types.KeyboardButton('СТОП!')
    btn_shuriken = types.KeyboardButton('Сюрикен')
    btn_cancel = types.KeyboardButton('Отменить сюрикен')
    keyboard.row(btn_turn, btn_stop)
    keyboard.row(btn_shuriken, btn_cancel)
    return keyboard


def place_hand_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_stop = types.KeyboardButton('СТОП!')
    btn_remove = types.KeyboardButton('Отпустить руку')
    keyboard.row(btn_stop, btn_remove)
    return keyboard


def stop_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_resume = types.KeyboardButton('Продолжить')
    keyboard.row(btn_resume)
    return keyboard


def concentration_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_release_hand = types.KeyboardButton('Отпустить руку')
    keyboard.row(btn_release_hand)
    return keyboard


def empty_keyboard():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard


def start_level_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    btn_start_level = types.KeyboardButton('Начать уровень')
    keyboard.row(btn_start_level)
    return keyboard
