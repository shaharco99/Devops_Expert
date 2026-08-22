import sys

from games import CurrencyRouletteGame, GuessGame, MemoryGame
from games.Live import difficulty, load_game, welcome

name = input("What is your name: ")
welcome(name)
while True:
    game = load_game()
    if game == "q":
        sys.exit()
    diff = int(difficulty())
    if int(game) == 1:
        MemoryGame.play(diff)
    elif int(game) == 2:
        GuessGame.play(diff)
    #      int(game) == 3
    else:
        CurrencyRouletteGame.play(diff)
