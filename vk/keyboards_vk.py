from vk_api.keyboard import VkKeyboard


def begin_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Участвую', 'default')
    keyboard.add_button('Начать игру', 'positive')
    return keyboard.get_keyboard()


def game_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Ход', 'positive')
    keyboard.add_button('СТОП!', 'negative')
    keyboard.add_line()
    keyboard.add_button('Сюрикен', 'primary')
    keyboard.add_button('Отменить сюрикен', 'default')
    return keyboard.get_keyboard()


def place_hand_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('СТОП!', 'negative')
    keyboard.add_button('Отпустить руку', 'positive')
    return keyboard.get_keyboard()


def stop_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Продолжить', 'positive')
    return keyboard.get_keyboard()


def concentration_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Отпустить руку', 'positive')
    return keyboard.get_keyboard()


def empty_keyboard():
    return VkKeyboard.get_empty_keyboard()


def start_level_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Начать уровень', 'positive')
    return keyboard.get_keyboard()
