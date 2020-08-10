from game import Game


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


class GameInterface:
    """Interface to the Game class

    GameInterface(send_message, send_dms)
    + send_message(chat_id, text, keyboard=None):
          function that is responsible for sending a single message
          to a dialogue or a person with a specific keyboard attached
    + send_dms(dict {user: message}):
          function that is responsible for sending direct messages
          to several users (one message per user)
    """

    games = {}
    players = {}

    def __init__(self, send_message_function: callable, send_dms_function: callable):
        self.send_message = send_message_function
        self.send_dms = send_dms_function

    def win(self, game_id):
        """Finish game and indicate victory"""
        self.games.pop(game_id)
        self.send_message(game_id,
                          'Ура, вы победили!',
                          'no_game')

    def lose(self, game_id):
        """Finish game and indicate defeat"""
        self.games.pop(game_id)
        self.send_message(game_id,
                          'Вы проиграли :(',
                          'no_game')

    def offer_next_level(self, status, game_id):
        """Offer players to proceed to next level"""
        rewards = [0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 0, 0]
        prizes = {2: "Сюрикен", 1: "Дополнительная жизнь", 0: "Ничего"}

        self.send_message(game_id, f"Уровень {status['level']} завершён!")
        self.send_message(game_id, f"Ваша награда: {prizes[rewards[status['level'] - 1]]}")
        self.send_message(game_id, f"Чтобы перейти к следующему уровню, нажмите \"Начать уровень\".",
                          keyboard="next_level_offer")

    def send_game_status(self, status, game_id):
        """Send information about HP and shurikens left"""
        text = f"Жизни: {status['hp']}\n" \
               f"Сюрикены: {status['n_shurikens']}"
        if sum(map(sum, status['player_hands'].values())) != 0:
            text += '\n\nКарт в руке:'
            for player, hand in status['player_hands'].items():
                text += f"\n{self.players[player].first_name}: {len(hand)}"
        self.send_message(game_id, text)

    def check_status(self, status, game_id):
        """React to victory, defeat of end of the level"""
        # game_status(status, message)
        if status['status'] == WIN:
            self.win(game_id)
        elif status['status'] == LOSE:
            self.lose(game_id)
        elif status['status'] == FREE_CHAT:
            self.offer_next_level(status, game_id)

    def print_droppile(self, status, game_id):
        """Tell what cards are discarded"""
        ll = status['discarded'].values()
        cards = list(map(str, sorted([el for lst in ll for el in lst])))
        cards = 'Сброшенные карты: ' + ', '.join(cards)
        self.send_message(game_id, cards,
                          keyboard='game')

    def dm_player_hands(self, status, game_id):
        """Tell players about cards of their hands"""
        dms = {}            # direct messages
        for player_id, hand in status['player_hands'].items():
            text = f"На руке: {' '.join(map(str, hand))}"
            dms[player_id] = text
        self.send_dms(dms)

    def start_level(self, game_id):
        """Start next level"""
        status = self.games[game_id].start_level()
        if status['response'] == LEVEL_STARTED:
            self.send_message(game_id,
                              "Концентрация. Поднимите руки со стола, когда будете готовы начинать.",
                              keyboard='concentration')
            self.dm_player_hands(status, game_id)
        else:
            print('WARNING')
            print(status)
            self.send_message(game_id,
                              'Что-то пошло не так :(\n'
                              'Если проблема повторяется, скорее всего, мы уже решаем её.')

    def init_user(self, user_id):
        """Send welcome message to user"""
        self.send_message(user_id,
                          'Отлично, я могу писать тебе сообщения! '
                          'Сюда ты будешь получать информацию о своих '
                          'картах.\nСоздай беседу с друзьями и добавь меня '
                          'туда, чтобы поиграть!',
                          keyboard='user_help')

    def init_dialogue(self, game_id, silent=False):
        """Prepare to run games in the dialogue; send a welcome message is not silent"""
        new_game = Game(game_id)
        self.games[game_id] = new_game
        if not silent:
            self.send_message(game_id,
                              "Речь мне не написали, но играть со мной уже можно",
                              keyboard='no_game')

    # Участвую
    def add_player(self, game_id, user_id):
        """Add player to a not started game"""
        status = self.games[game_id].add_player(user_id)
        if status['response'] == WARNING:
            self.send_message(game_id,
                              "Ты уже участвуешь или максимальное количество игроков достигнуто",
                              keyboard='no_game')
        else:
            self.players[user_id] = 1  # было: ... = user | Что это? Зачем хранить пользователя? todo
            self.send_message(game_id,
                              f"Ты в игре! Колическтво игроков: {len(status['player_hands'])}",
                              keyboard='no_game')

    # Начать игру
    def start_game(self, game_id):
        """Start new game if there are enough players"""
        chat_id = game_id
        status = self.games[chat_id].start_game()
        if len(status['player_hands']) < 2:
            self.send_message(game_id, 'Для начала игры нужно хотя бы 2 игрока',
                              keyboard='no_game')
        else:
            self.send_message(game_id, 'Начинаем!')
            self.start_level(game_id)

    # Закончить игру
    def end_game(self, game_id):
        """Force finish game"""
        self.games.pop(game_id)
        self.send_message(game_id,
                          'Игра завершена. Чтобы начать новую игру, нажмите [какую-то кнопку]',
                          keyboard='no_game')

    # Ход
    def act(self, game_id, user_id):
        """Place a card as a player"""
        status = self.games[game_id].act(user_id)
        if status['response'] != WARNING:
            card_played = str(status['top_card'])
            self.send_message(game_id,
                              'Сыгранная карта: ' + card_played,
                              keyboard='in-game')
            self.dm_player_hands(status, game_id)
            if sum(map(sum, status['discarded'].values())) != 0:
                self.send_message(game_id, "Упс, ошибочка вышла :(")
                self.print_droppile(status, game_id)

        self.check_status(status, game_id)

    # Стоп!
    def stop(self, game_id, user_id):
        self.send_message(game_id,
                          'СТОП! Если хотите продолжить - все должны отпустить руки',
                          keyboard='place_hand')
        self.games[game_id].place_hand(user_id)

    # Отпустить руку
    def player_concentration(self, game_id, user_id):
        status = self.games[game_id].release_hand(user_id)
        if status['response'] == CONCENTRATION_ENDS:
            self.send_message(game_id, "Можно играть!",
                              keyboard='in-game')
            self.dm_player_hands(status, game_id)

    # Сюрикен
    def shuriken(self, game_id, user_id):
        # TODO Отправить сообщение о голосовании за сюрикен со статусом голосования
        status = self.games[game_id].vote_shuriken(user_id)
        if status['response'] == SHURIKEN_THROWN:
            self.send_message(game_id, "Сюрикен!")
            self.print_droppile(status, game_id)
            self.dm_player_hands(status, game_id)
            self.check_status(status, game_id)

    # Отменить сюрикен
    def cancel(self, game_id, user_id):
        self.games[game_id].release_hand(user_id)
