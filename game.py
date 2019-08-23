import random
from itertools import dropwhile

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


def throw_warning(text):
    print('WARNING: ' + text)


class Game:
    # initialized on init
    # initialized on start
    # initialized on compilation
    rewards = [0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1]


    def __init__(self, game_id):
        self.game_id = game_id
        self.n_levels = None
        self.hp = None
        self.n_players = 0
        self.player_hands = dict()
        self.player_status = dict()
        self.level = 0
        self.status = 0
        self.n_shurikens = 1
        self.top_card = 0

    # add a player to the unstarted game session
    def add_player(self, player_id):
        response = PLAYER_ADDED
        if self.status == NOT_STARTED:
            if player_id in self.player_hands.keys():
                response = WARNING
                throw_warning('The player has been already added to the game. '
                              'This call is ignored.')
            else:
                self.player_hands[player_id] = list()
                self.player_status[player_id] = NORMAL
                self.n_players += 1
        else:
            response = WARNING
            throw_warning('A player was added after the game was started. '
                          'This player will not take part in this game.')
        return self.__get_status(response)

    def start_game(self, player_id):
        response = GAME_STARTED
        if self.status == NOT_STARTED and player_id in self.player_hands.keys():
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
                response = WARNING
                throw_warning("n_levels should be either 2, 3, or 4. "
                              "This call is ignored.")
            if response != WARNING:
                self.status = FREE_CHAT
        else:
            response = WARNING
            throw_warning(
                'It was tried to start the game when it had already been started. '
                'This call is ignored.')
        return self.__get_status(response)

    # proceed to the next level
    def start_level(self, player_id):
        response = LEVEL_STARTED
        if self.status == FREE_CHAT and player_id in self.player_hands.keys():
            self.level += 1
            self.status = ACTION
            self.__pass_cards(self.level)
            # everyone places their hand on the table
            for player_id in self.player_status.keys():
                self.place_hand(player_id)
        else:
            response = WARNING
            throw_warning(
                'It was tried to start a level when other level is not finished. '
                'This call is ignored.')
        return self.__get_status(response)

    # place a card to the stack
    def act(self, player_id):
        response = CARD_PLAYED
        discarded = {player_id: list() for player_id in
                     self.player_status.keys()}
        if self.status == ACTION and player_id in self.player_hands.keys() and \
                self.player_hands[player_id]:
            card = min(self.player_hands[player_id])
            self.player_hands[player_id].remove(card)
            self.top_card = card
            flag = False
            for player_id in self.player_hands.keys():
                new_hand = list(
                    dropwhile(lambda x: x < card, self.player_hands[player_id]))
                if new_hand != self.player_hands[player_id]:
                    flag = True
                    discarded[player_id] = [item for item in
                                            self.player_hands[player_id] if
                                            item not in new_hand]
                    self.player_hands[player_id] = new_hand
            if flag:
                self.hp -= 1
                if self.hp < 0:
                    self.status = LOSE
            if sum(map(sum, self.player_hands.values())) == 0 and \
                    self.hp >= 0:
                self.__finish_level()
        else:
            response = WARNING
            throw_warning('Something went wrong when playing a card. '
                          'This call is ignored.')
        return self.__get_status(response, discarded=discarded)

    def place_hand(self, player_id):
        response = HAND_PLACED
        if self.status in [CONCENTRATION,
                           ACTION] and player_id in self.player_hands.keys():
            self.player_status[player_id] = STOP
            if self.status != CONCENTRATION:
                response = CONCENTRATION_BEGINS
            self.status = CONCENTRATION
        else:
            response = WARNING
            throw_warning('Hand was placed during wrong game phase. '
                          'This call is ignored.')
        return self.__get_status(response)

    # change hand state to NORMAL
    # called when unvoting for shuriken or being ready to end concentration
    def release_hand(self, player_id):
        response = HAND_RELEASED
        if player_id in self.player_hands.keys() and self.player_status[
            player_id] == STOP:
            self.player_status[player_id] = NORMAL
            if STOP not in self.player_status.values():
                self.status = ACTION
                response = CONCENTRATION_ENDS
        elif player_id in self.player_hands.keys() and self.player_status[
            player_id] == SHURIKEN:
            self.player_status[player_id] = NORMAL
        else:
            response = WARNING
            throw_warning('Player s hand had been already released. '
                          'This call is ignored.')
        return self.__get_status(response)

    def vote_shuriken(self, player_id):
        response = VOTED_FOR_SHURIKEN
        discarded = {player_id: list() for player_id in
                     self.player_status.keys()}
        if player_id in self.player_hands.keys() and self.status == ACTION and \
                self.n_shurikens > 0:
            self.player_status[player_id] = SHURIKEN
            if list(self.player_status.values()).count(SHURIKEN) == \
                    len(self.player_status.values()):
                response = SHURIKEN_THROWN
                self.n_shurikens -= 1
                for player_id in self.player_hands.keys():
                    if self.player_hands[player_id]:
                        discarded[player_id] = [
                            min(self.player_hands[player_id])]
                        self.player_hands[player_id].remove(
                            min(self.player_hands[player_id]))
                    self.player_status[player_id] = NORMAL
            if sum(map(sum, self.player_hands.values())) == 0:
                self.__finish_level()
        else:
            response = WARNING
            throw_warning('Something went wrong during voting for shuriken. '
                          'This call is ignored.')
        return self.__get_status(response, discarded=discarded)

    def load_status(self, status_dict):
        self.game_id = status_dict['game_id']
        self.n_players = len(status_dict['player_hands'].keys())

        # calculate n_levels
        self.status = NOT_STARTED
        self.start_game()

        self.hp = status_dict['hp']
        self.player_hands = status_dict['player_hands']
        self.player_status = status_dict['player_status']
        self.level = status_dict['level']
        self.status = status_dict['status']
        self.n_shurikens = status_dict['n_shurikens']
        self.top_card = status_dict['top_card']

        return self.__get_status(status_dict['response'])

    def __check_stop_status(self):
        flag = True
        for status in self.player_status.values():
            if status != STOP:
                flag = False
        return flag

    def __check_concentration_status(self):
        flag = True
        for status in self.player_status.values():
            if status == CONCENTRATION:
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
            self.player_hands[player_id] = sorted(
                deck[i * n_cards: (i + 1) * n_cards])
            print(self.player_hands[player_id])
            print("as set: ", set(self.player_hands[player_id]))

    # finish the current level
    def __finish_level(self):
        if self.status == ACTION or \
                self.status == CONCENTRATION:
            if self.level == self.n_levels:
                self.status = WIN
            else:
                self.status = FREE_CHAT
                if self.rewards[self.level - 1] == 2:
                    self.n_shurikens = min(3, self.n_shurikens + 1)
                if self.rewards[self.level - 1] == 1:
                    self.hp = min(5, self.hp + 1)

    # returns the current game state as dict object
    # this object must be returned by every public function
    def __get_status(self, response, discarded=dict()):
        return {'response': response,
                'status': self.status,
                'game_id': self.game_id,
                'n_shurikens': self.n_shurikens,
                'hp': self.hp,
                'player_hands': self.player_hands,
                'player_status': self.player_status,
                'top_card': self.top_card,
                'level': self.level,
                'discarded': {player_id: discarded.get(player_id, [])
                              for player_id in self.player_status.keys()}}


if __name__ == '__main__':
    game = Game(3)
    print(game.start_level())
    print(game.act(1, 1))
