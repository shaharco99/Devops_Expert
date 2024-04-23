from games import CurrencyRouletteGame, GuessGame, MemoryGame
from games.Live import welcome,load_game,difficulty
from MainScores import read_score,write_score


player = input("What is your name: ")
welcome(player)

score = read_score(player)

if score is not None:
    print(f"Your current score is: {score}")
else:
    print("User not found. Creating a new user.")
    write_score(player, 0)
    print(f"New user {player} created with score 0.")

while True:
    game = load_game()
    if game == "q":
        exit()
    diff = int(difficulty())
    if int(game) == 1:
        MemoryGame.play(diff,player)
    elif int(game) == 2:
        GuessGame.play(diff,player)
    #      int(game) == 3
    else:
        CurrencyRouletteGame.play(diff,player)
