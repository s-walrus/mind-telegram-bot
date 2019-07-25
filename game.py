import random


class Game:

    n_levels = None
    n_players = None
    hp = None
    players = None
    level = 0
    level_started = False
    rewards = [0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1]
    n_bombs = 1

    def __init__ (self, n_players):
        self.n_players = n_players
        self.players = [[] for _ in range(n_players)]
        if n_players == 2:
            self.n_levels = 12
            self.hp = 2
        elif n_players == 3:
            self.n_levels = 10
            self.hp = 3
        elif n_players == 4:
            self.n_levels = 8
            self.hp = 4
        else:
            raise ValueError("n_levels should be either 2, 3, or 4")

    def pass_cards(self, n_cards):
        deck = list(range(1, 101))
        random.shuffle(deck)
        res = [[] for _ in range(self.n_players)]
        print(n_cards)
        for i in range(self.n_players):
            res[i] = deck[i * n_cards : (i+1) * n_cards]
        return res


    def start_level(self, force=False):
        if not self.level_started or force:
            self.level += 1
            self.level_started = True
            res = self.pass_cards(self.level)
            return res
        else:
            print("It was attempted to start a level before finishing the previous one. Use 'start_leve(force=True)' to force start a level.")


if __name__ == '__main__':
    game = Game(2)
    print(game.start_level())

