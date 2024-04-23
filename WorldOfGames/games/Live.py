
def welcome(player):
    # This function greets the user with his name
    return print(f"Hello {player} and welcome to the Word of Games(Wog).\nHere you can find many cool games to play.")
    


def load_game():
    # This function asks the user what game he wants to play
    game = input("""Please choose a game to play:
    1. Memory Game - a sequence of numbers will appear for 0.7 second and you have to guess it back
    2. Guess Game - guess a number and see if you chose like the computer
    3. Currency Roulette - try and guess the value of a random amount of USD in ILS
* if you want to quit press 'q'
""")
    return valid_num(1, 3, game)


def difficulty():
    # This function asks the user what difficulty he wants to play
    diff = input("please choose game difficulty from 1 (easiest) to 5 (hardest): ")
    return valid_num(1, 5, diff)


def valid_num(minimum, maximum, item):
    # This function validit an item between minimum - maximum
    while True:
        if type(item) != "int":
            if item.isdigit():
                if minimum <= int(item) <= maximum:
                    return item
                else:
                    item = input(f"please enter a number between {minimum} - {maximum}: ")
            else:
                if item == "q":
                    return item
                else:
                    item = input(f"your input is not a number, please enter a number between {minimum} - {maximum}: ")
