import random


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
                'player_hands': self.player_hands}

    # add a player to the unstarted game session
    def add_player(self, player_id):
        if self.status == self.__NOT_STARTED:
            self.player_hands[player_id] = set()
            self.player_stops[player_id] = False
            self.n_players += 1
        else:
            raise RuntimeError('A player was added after the game had been started.')
        return self.get_status()

    def start_game(self):
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
            self.status = self.__CONCENTRATION
            self.pass_cards(self.level)
            # everyone places their hand on the table
            for player_id in self.player_stops.keys():
                self.place_hand(player_id)
        return self.get_status()

    # TODO act(self, player_id) -> play the lowest card
    # place a card to the stack
    def act(self, player_id, card):
        if self.status == self.__ACTION and card in self.player_hands[player_id]:
            self.player_hands[player_id].remove(card)
            self.top_card = card
            flag = False
            for hand in self.player_hands:
                for c in hand:
                    if c < card:
                        flag = True
                        hand.remove(c)
            if flag:
                self.hp -= 1
                if self.hp < 0:
                    self.status = self.__LOSE
                    self.game_over()
            if sum(map(sum, self.player_hands.values())) == 0:
                self.finish_level()
        else:
            print("It was attempted to play a card not being held by the player. " +
                  "Use 'act(player_id, card, force=True)' " +
                  "to force play a card.")

        return self.get_status()

    def place_hand(self, player_id):
        if self.status == self.__ACTION:
            self.player_stops[player_id] = True
            self.status = self.__CONCENTRATION

    def release_hand(self, player_id):
        if self.status == self.__CONCENTRATION:
            self.player_stops[player_id] = False
            if sum(self.player_stops.values()) == 0:
                self.status = self.__ACTION
        return self.get_status()

    def stop(self, player_id):
        self.place_hand(player_id)
        return self.get_status()

    def use_shuriken(self):
        if self.status == self.__ACTION and \
                self.n_shurikens > 0:
            self.n_shurikens -= 1
            for hand in self.player_hands:
                if not hand.empty():
                    hand.remove(min(hand))
                    # TODO send discarded cards in status


if __name__ == '__main__':
    game = Game(3)
    print(game.start_level())
    print(game.act(1, 1))
