import random


class Game:

    n_levels = None
    n_players = None
    hp = None
    player_hands = None
    level = 0
    level_started = False
    rewards = [0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1]
    n_bombs = 1

    def __init__ (self, n_players):
        self.n_players = n_players
        self.player_hands = [set() for _ in range(n_players)]
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
        res = [set() for _ in range(self.n_players)]
        for i in range(self.n_players):
            res[i] = set(deck[i * n_cards : (i+1) * n_cards])
        return res


    def start_level(self, force=False):
        if not self.level_started or force:
            self.level += 1
            self.level_started = True
            self.player_hands = self.pass_cards(self.level)
        else:
            print("It was attempted to start a level before \
                   finishing the previous one. Use 'start_leve(force=True)' \
                   to force start a level.")
        return self.player_hands

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
                hp -= 1
        else:
            print("It was attempted to play a card not being held by the player. \
                    Use 'act(player_id, card, force=True)' \
                    to force play a card.")
        return self.player_hands


if __name__ == '__main__':
    game = Game(2)
    print(game.start_level())
    print(game.act(1, 1))

