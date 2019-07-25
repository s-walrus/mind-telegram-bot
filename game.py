import random


class Game:
    # initialized on init
    game_id = None
    # initialized on start
    n_levels = None
    hp = None
    # initialized on compilation
    n_players = 0
    player_hands = dict()
    player_stops = dict()
    level = 0
    level_started = False
    game_started = False
    is_stopped = False
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
        self.level_started = False

    # returns the current game state as dict object
    # this object is returned by every public function
    def get_status(self):
        return {'game_started': self.game_started,
                'game_id': self.game_id,
                'n_shurikens': self.n_shurikens,
                'hp': self.hp,
                'player_hands': self.player_hands}

    # add a player to the unstarted game session
    def add_player(self, player_id):
        if not self.game_started:
            self.player_hands[player_id] = set()
            self.n_players += 1
        else:
            raise RuntimeError('A player was added after the game had been started.')
        return self.get_status()

    def start_game(self):
        self.game_started = True
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
    # use force=True to start the next level
    # before finishing the currect one
    def start_level(self, force=False):
        if not self.level_started or force:
            self.level += 1
            self.level_started = True
            self.pass_cards(self.level)
        else:
            print("It was attempted to start a level before " +
                  "finishing the previous one. Use 'start_level(force=True)' " +
                  "to force start a level.")
        return self.get_status()

    # place a card to the stack
    def act(self, player_id, card):
        if card in self.player_hands[player_id]:
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
                    self.game_over()
            if sum(map(sum, self.player_hands.values())) == 0:
                self.finish_level()
        else:
            print("It was attempted to play a card not being held by the player. " +
                  "Use 'act(player_id, card, force=True)' " +
                  "to force play a card.")

        return self.get_status()


if __name__ == '__main__':
    game = Game(3)
    print(game.start_level())
    print(game.act(1, 1))
