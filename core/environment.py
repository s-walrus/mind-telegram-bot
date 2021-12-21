from game import Game

if __name__ == "__main__":
    game = Game(42)
    while True:
        action = input()
        eval("print(game." + action + ")")
