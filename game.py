import random
from itertools import dropwhile


class Game:
    # constants
    __NOT_STARTED = 0
    __FREE_CHAT = 1
    __CONCENTRATION = 2
    __ACTION = 3
    __WIN = 4
    __LOSE = 5
    __STOP = 0
    __NORMAL = 1
    __SHURIKEN = 2
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

    # randomly gives cards to each player as it is done
    # at the start of every level
    def pass_cards(self, n_cards):
        deck = list(range(1, 101))
        random.shuffle(deck)
        for i, player_id in enumerate(self.player_hands.keys()):
            self.player_hands[player_id] = set(deck[i * n_cards: (i + 1) * n_cards])

    # called when the game is failed
    def game_over(self):
        pass

    # finish the current level
    def finish_level(self):
        if self.status == self.__ACTION or \
                self.status == self.__CONCENTRATION:
            if self.level == self.n_levels:
                self.status = self.__WIN
            else:
                self.status = self.__FREE_CHAT

    # returns the current game state as dict object
    # this object is returned by every public function
    def get_status(self):
        return {'status': self.status,
                'game_id': self.game_id,
                'n_shurikens': self.n_shurikens,
                'hp': self.hp,
                'player_hands': self.player_hands,
                'player_status': self.player_status,
                'top_card': self.top_card}

    # add a player to the unstarted game session
    def add_player(self, player_id):
        if self.status == self.__NOT_STARTED:
            self.player_hands[player_id] = set()
            self.player_status[player_id] = self.__NORMAL
            self.n_players += 1
        else:
            raise RuntimeError('A player was added after the game had been started.')
        return self.get_status()

    def start_game(self):
        print(self.n_players)
        if self.status == self.__NOT_STARTED:
            self.status = self.__FREE_CHAT
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
        return self.get_status()

    # proceed to the next level
    def start_level(self):
        if self.status == self.__FREE_CHAT:
            self.level += 1
            self.status = self.__ACTION
            self.pass_cards(self.level)
            # everyone places their hand on the table
            for player_id in self.player_status.keys():
                self.place_hand(player_id)
        return self.get_status()

    # TODO act(self, player_id) -> play the lowest card
    # place a card to the stack
    def act(self, player_id):
        if self.status == self.__ACTION and self.player_hands[player_id]:
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
                    self.status = self.__LOSE
                    self.game_over()
            if sum(map(sum, self.player_hands.values())) == 0:
                self.finish_level()
        return self.get_status()

    def place_hand(self, player_id):
        if self.status in [self.__CONCENTRATION, self.__ACTION]:
            self.player_status[player_id] = self.__STOP
            self.status = self.__CONCENTRATION

    def release_hand(self, player_id):
        if self.status == self.__CONCENTRATION:
            self.player_status[player_id] = self.__NORMAL
            if self.__STOP not in self.player_status.values():
                self.status = self.__ACTION
        return self.get_status()

    def stop(self, player_id):
        self.place_hand(player_id)
        return self.get_status()

    def vote_shuriken(self, player_id):
        if self.status == self.__ACTION and \
                self.n_shurikens > 0:
            self.player_status[player_id] = self.__SHURIKEN
            if self.player_status.values().count(self.__SHURIKEN) == \
                    len(self.player_status.values()):
                self.n_shurikens -= 1
                for hand in self.player_hands:
                    if not hand.empty():
                        hand.remove(min(hand))
                        # TODO send discarded cards in status
                for player_id in self.player_status.keys():
                    self.player_status[player_id] = self.__NORMAL
        return self.get_status()

    def unvote_shuriken(self, player_id):
        if self.player_status[player_id] == self.__SHURIKEN:
            self.player_status[player_id] = self.__NORMAL
        return self.get_status()

    def check_stop_status(self):
        flag = True
        for status in self.player_status.values():
            if status != self.__STOP:
                flag = False
        return flag

    def check_concentration_status(self):
        flag = True
        for status in self.player_status.values():
            if status == self.__CONCENTRATION:
                flag = False
        return flag

    def release_hands_all(self):
        for player in self.player_status.keys():
            self.release_hand(player)


if __name__ == '__main__':
    game = Game(3)
    print(game.start_level())
    print(game.act(1, 1))
