import random
from itertools import dropwhile


class Game:
    # game phases
    _NOT_STARTED = 0
    _FREE_CHAT = 1
    _CONCENTRATION = 2
    _ACTION = 3
    _WIN = 4
    _LOSE = 5
    # player status
    _STOP = 0
    _NORMAL = 1
    _SHURIKEN = 2
    # initialized on init
    game_id = None
    # initialized on start
    n_levels = None
    hp = None
    # initialized on compilation
    n_players = 0
    player_hands = dict()
    player_status = dict()
    level = 0
    status = 0
    rewards = [0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1]
    n_shurikens = 1
    top_card = 0

    def __init__(self, game_id):
        self.game_id = game_id

    # add a player to the unstarted game session
    def add_player(self, player_id):
        if self.status == self._NOT_STARTED:
            self.player_hands[player_id] = set()
            self.player_status[player_id] = self._NORMAL
            self.n_players += 1
        else:
            raise RuntimeError('A player was added after the game had been started.')
        return self.__get_status()

    def start_game(self):
        if self.status == self._NOT_STARTED:
            self.status = self._FREE_CHAT
            if self.n_players == 2:
                self.n_levels = 12
                self.hp = 2
            elif self.n_players == 3:
                self.n_levels = 10
                self.hp = 3
            elif self.n_players == 4:
                self.n_levels = 8
                self.hp = 4
            else:
                raise ValueError("n_levels should be either 2, 3, or 4")
        return self.__get_status()

    # proceed to the next level
    def start_level(self):
        if self.status == self._FREE_CHAT:
            self.level += 1
            self.status = self._ACTION
            self.__pass_cards(self.level)
            # everyone places their hand on the table
            for player_id in self.player_status.keys():
                self.place_hand(player_id)
        return self.__get_status()

    # place a card to the stack
    def act(self, player_id):
        if self.status == self._ACTION and self.player_hands[player_id]:
            card = min(self.player_hands[player_id])
            self.player_hands[player_id].remove(card)
            self.top_card = card
            flag = False
            for player_id in self.player_hands.keys():
                new_hand = set(dropwhile(lambda x: x < card, self.player_hands[player_id]))
                if new_hand != self.player_hands[player_id]:
                    flag = True
                    self.player_hands[player_id] = new_hand
            if flag:
                self.hp -= 1
                if self.hp < 0:
                    self.status = self._LOSE
                    self.game_over()
            if sum(map(sum, self.player_hands.values())) == 0:
                self.__finish_level()
        return self.__get_status()

    def place_hand(self, player_id):
        if self.status in [self._CONCENTRATION, self._ACTION]:
            self.player_status[player_id] = self._STOP
            self.status = self._CONCENTRATION

    def release_hand(self, player_id):
        if self.status == self._CONCENTRATION:
            self.player_status[player_id] = self._NORMAL
            if self._STOP not in self.player_status.values():
                self.status = self._ACTION
        return self.__get_status()

    def stop(self, player_id):
        self.place_hand(player_id)
        return self.__get_status()

    def vote_shuriken(self, player_id):
        if self.status == self._ACTION and \
                self.n_shurikens > 0:
            self.player_status[player_id] = self._SHURIKEN
            if list(self.player_status.values()).count(self._SHURIKEN) == \
                    len(self.player_status.values()):
                self.n_shurikens -= 1
                for hand in self.player_hands.values():
                    if hand:
                        hand.remove(min(hand))
                        # TODO send discarded cards in status
                for player_id in self.player_status.keys():
                    self.player_status[player_id] = self._NORMAL
        return self.__get_status()

    def unvote_shuriken(self, player_id):
        if self.player_status[player_id] == self._SHURIKEN:
            self.player_status[player_id] = self._NORMAL
        return self.__get_status()

    def load_status(self, status_dict):
        self.game_id = status_dict['game_id']
        self.n_players = len(status_dict['player_hands'].keys())

        # calculate n_levels
        self.status = self._NOT_STARTED
        self.start_game()

        self.hp = status_dict['hp']
        self.player_hands = status_dict['player_hands']
        self.player_status = status_dict['player_status']
        self.level = status_dict['level']
        self.status = status_dict['status']
        self.n_shurikens = status_dict['n_shurikens']
        self.top_card = status_dict['top_card']

        return self.__get_status()

    def __check_stop_status(self):
        flag = True
        for status in self.player_status.values():
            if status != self._STOP:
                flag = False
        return flag

    def __check_concentration_status(self):
        flag = True
        for status in self.player_status.values():
            if status == self._CONCENTRATION:
                flag = False
        return flag

    def __release_hands_all(self):
        for player in self.player_status.keys():
            self.release_hand(player)

    # give random cards to each player
    def __pass_cards(self, n_cards):
        deck = list(range(1, 101))
        random.shuffle(deck)
        for i, player_id in enumerate(self.player_hands.keys()):
            self.player_hands[player_id] = set(deck[i * n_cards: (i + 1) * n_cards])

    # finish the current level
    def __finish_level(self):
        if self.status == self._ACTION or \
                self.status == self._CONCENTRATION:
            if self.level == self.n_levels:
                self.status = self._WIN
            else:
                self.status = self._FREE_CHAT

    # returns the current game state as dict object
    # this object is returned by every public function
    def __get_status(self):
        return {'status': self.status,
                'game_id': self.game_id,
                'n_shurikens': self.n_shurikens,
                'hp': self.hp,
                'player_hands': self.player_hands,
                'player_status': self.player_status,
                'top_card': self.top_card,
                'level': self.level}


if __name__ == '__main__':
    game = Game(3)
    print(game.start_level())
    print(game.act(1, 1))
