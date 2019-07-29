import random


def get_cards(player_count, level):
    cards = []
    a = [i for i in range(1, 101)]
    random.shuffle(a)
    for i in range(player_count):
        cards.append([])
        for j in range(level):
            cards[i].append(a[i * level + j])

    return cards


a = get_cards(2, 2)
print(a)
